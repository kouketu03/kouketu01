import io  
import sys
import requests
from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
from collections import defaultdict
import math
from dicmysql import Mysql


class NaiveBayes:

	def __init__(self):
		self.Mysql = Mysql()
		self.POSSITIVE = 1
		self.NEGATIVE = 2

	def get_words(self):
		vocabularies = self.Mysql.get_vocabularise()
		return vocabularies

	def words_in_cat(self,category):
		words_in_cat = self.Mysql.get_words_in_cat(category)
		return words_in_cat

	def word_count_in_cat(self, word,category):
		word_count_in_cat = self.Mysql.get_word_in_cat(word,category)
		return word_count_in_cat
	
	def all_cats_count(self):
		all_cat_count = self.Mysql.get_all_cats_count()
		return all_cat_count
	
	def cat_count(self, category):
		cat_count = self.Mysql.get_cat_count(category)
		return cat_count

	def word_count(self,word):
		word_count =self.Mysql.get_word_count(word)
		return word_count

	def word_in_cat_probability(self,word, category):
	#p(word|cat)を計算する
	#ラプラススムージング を適用
		vocabularies     = self.get_words()
		words_in_cat     = self.words_in_cat(category)
		word_count       = self.word_count_in_cat(word,category) + 1
		vocabulary_count = len(words_in_cat) + len(vocabularies) #取得した配列の最後に''要素があるから、それを消す
		return float(word_count) / float(vocabulary_count)

	def cat_probability(self,category):
	#p(cat)を計算する
		all_cats_count = self.all_cats_count()
		cat_count = self.cat_count(category)
		return float(cat_count) / float(all_cats_count)

	def word_probability(self,word):
	#p(word)を計算する
	#ラプラススムージング を適用
		vocabularies     = self.get_words()
		word_count       = self.word_count(word) + 1
		return float(word_count) / float(len(vocabularies)*2)#ラプラススムージングの為にlen(vocabularies)　+len(vocabularies)を掛ける２にしました。

	def cat_if_document(self,document, category):
	#p(cat|document)を計算する
	#p(cat|document) = p(document|cat)*p(cat)/p(document)
					#= p(word1|cat)*p(word2|cat)*...p(wordn|cat)*p(cat)/(p(word1)*p(word2)*p(word2)*...*p(wordn))
		cat_probability = math.log(self.cat_probability(category))

		words = self.Mysql.ja_tokenize(document)
		word_in_cat_probability = 0
		word_probability = 0
		for word in words:
			word_in_cat_probability +=  math.log(self.word_in_cat_probability(word, category))
			word_probability += math.log(self.word_probability(word))
		cat_if_document_probability = word_in_cat_probability + cat_probability - word_probability
		return cat_if_document_probability

	def document_classify(self, document):

		document_possitive_p = self.cat_if_document(document, self.POSSITIVE)
		document_negative_p = self.cat_if_document(document, self.NEGATIVE)

		p_list = [document_possitive_p ,document_negative_p]

		document_cat_num = 0
		if max(p_list) == document_possitive_p:
			document_cat = 'pos'
			document_cat_num += 1

		if max(p_list) == document_negative_p:
			document_cat = 'neg'
			document_cat_num += 2
		print(document)
		self.Mysql.insert_into_db(document,document_cat_num)
		return document_cat

	def word_classify(self, word):

		html = requests.get('https://www.google.co.jp/search?q=' +word).content
		soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
		dicriptions = soup.find_all("div", class_="g")
		z = []
		for dicription in dicriptions:
			z.append(dicription.get_text())
		document_classify = []
		for o in z:
			document_classify.append(self.document_classify(o))
			#print('この記事のカテゴリー:'+ self.document_classify(o))
		possitive_num =  document_classify.count('pos')
		negative_num =  document_classify.count('neg')
		word_cat = ''
		if possitive_num > negative_num :
			word_cat += 'possitive'
		if possitive_num < negative_num :
			word_cat += 'negative'
		return word_cat

