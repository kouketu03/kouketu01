import pymysql
from janome.tokenizer import Tokenizer
import collections
class Mysql:
	DB_HOST = 'localhost'
	DB_USER = 'fuhyou'
	DB_PW = 'women637'
	DB_NAME = 'fuhyou'

	def connect_db(self):
		db = pymysql.connect(self.DB_HOST,self.DB_USER,self.DB_PW,self.DB_NAME,charset='utf8' )

		return db

	def ja_tokenize(self, sentences):
		ja_tokenizer=Tokenizer()
		res=[]
		for sentence in sentences:
			malist=ja_tokenizer.tokenize(sentence)

			for tok in malist:
				ps=tok.part_of_speech.split(",")[0]
				if not ps in ['名詞', '動詞', '形容詞']:continue
				w=tok.base_form
				if w=="*" or w=="": w=tok.surface
				if w=="" or w=="\n" or w=="...": continue
				res.append(w)
		return res

	def fuhyou_insert_sentence(self,sentences):
		ja_tokenizer=Tokenizer()
		conn = self.connect_db()
		cursor = conn.cursor()
		
		for sentence in sentences:
			malist=ja_tokenizer.tokenize(sentence)
			word_arr=[]
			for tok in malist:
				ps=tok.part_of_speech.split(",")[0]
				if not ps in ['名詞', '動詞', '形容詞']:continue
				w=tok.base_form
				if w=="*" or w=="": w=tok.surface
				if w=="" or w=="\n" or w=="...": continue
				word_arr.append(w)
			word_num = len(word_arr)
			cat = 0
			words = '';
			for word in word_arr:
				words += word + ','
			sql = 'INSERT INTO sentences( sentence, words, word_num, cat ) values("%s", "%s", "%d", "%d")' % \
			(pymysql.escape_string(sentence), pymysql.escape_string(words), word_num, cat)
			cursor.execute(sql)
			conn.commit()

	def insert_into_db(self,sentence,cat):
		ja_tokenizer=Tokenizer()
		conn = self.connect_db()
		cursor = conn.cursor()
		malist=ja_tokenizer.tokenize(sentence)
		word_arr=[]
		for tok in malist:
			ps=tok.part_of_speech.split(",")[0]
			if not ps in ['名詞', '動詞', '形容詞']:continue
			w=tok.base_form
			if w=="*" or w=="": w=tok.surface
			if w=="" or w=="\n" or w=="..." or w=="\"" or w=="[" or w=="=" or w=="@" or w==":" or w=="&" or w==";": continue
			word_arr.append(w)
		word_num = len(word_arr)
		words = '';
		for word in word_arr:
			words += word + ','
		sql = 'INSERT INTO sentences( sentence, words, word_num, cat ) values("%s", "%s", "%d", "%d")' % \
		(pymysql.escape_string(sentence), pymysql.escape_string(words), word_num, cat)
		cursor.execute(sql)
		conn.commit()		

	def get_word_in_cat(self,word,category):
		conn = self.connect_db()
		cursor = conn.cursor()
		sql = 'SELECT words FROM sentences WHERE cat = %d' % \
		(category)
		cursor.execute(sql)
		words_arr = cursor.fetchall()
		words_arr02 = []
		for per_word in words_arr:
			words_arr02.append(per_word[0])
		words_string = ''
		for a in words_arr02:
			words_string += a
		words_uncomplete = words_string.split(',')
		words = []
		for o in words_uncomplete:
			if o=="" or o=="\n" or o=="..." or o==".": continue
			words.append(o)
		word_count_in_cat = words.count(word)
		return word_count_in_cat

	def get_vocabularise(self):
		conn = self.connect_db()
		cursor = conn.cursor()
		sql = 'SELECT words FROM sentences'
		cursor.execute(sql)
		words_arr = cursor.fetchall()
		words_arr02 = []
		for per_word in words_arr:
			words_arr02.append(per_word[0])
		words_string = ''
		for a in words_arr02:
			words_string += a
		words_uncomplete = words_string.split(',')
		words = []
		for o in words_uncomplete:
			if o=="" or o=="\n" or o=="..." or o==".": continue
			words.append(o)
		return words

	def get_words_in_cat(self,category):
		conn = self.connect_db()
		cursor = conn.cursor()
		sql = 'SELECT words FROM sentences WHERE cat = %d' % \
		(category)
		cursor.execute(sql)
		words_arr = cursor.fetchall()
		words_arr02 = []
		for per_word in words_arr:
			words_arr02.append(per_word[0])
		words_string = ''
		for a in words_arr02:
			words_string += a
		words_uncomplete = words_string.split(',')
		words = []
		for o in words_uncomplete:
			if o=="" or o=="\n" or o=="..." or o==".": continue
			words.append(o)
		return words

	def get_all_cats_count(self):
		conn = self.connect_db()
		cursor = conn.cursor()
		sql = 'SELECT COUNT( cat ) FROM sentences WHERE cat != 0'
		cursor.execute(sql)
		all_cats_count = cursor.fetchone()

		return all_cats_count[0]

	def get_cat_count(self, category):
		conn = self.connect_db()
		cursor = conn.cursor()
		sql = 'SELECT COUNT( cat ) FROM sentences WHERE cat = %d' % \
		(category)
		cursor.execute(sql)
		cat_count = cursor.fetchone()
		return cat_count[0]

	def get_word_count(self,word):
		conn = self.connect_db()
		cursor = conn.cursor()
		sql = 'SELECT words FROM sentences'
		cursor.execute(sql)
		words_arr = cursor.fetchall()
		words_arr02 = []
		for per_word in words_arr:
			words_arr02.append(per_word[0])
		words_string = ''
		for a in words_arr02:
			words_string += a
		words_uncomplete = words_string.split(',')
		words = []
		for o in words_uncomplete:
			if o=="" or o=="\n" or o=="..." or o==".": continue
			words.append(o)
		word_count = words.count(word)
		return word_count

	def check_history_word(self,word):
		conn = self.connect_db()
		cursor = conn.cursor()
		sql = 'SELECT cat FROM history_words WHERE words = "%s"' % \
		(word)
		cursor.execute(sql)
		cat_count = cursor.fetchone()
		if cat_count == None:
			return 'nothing'
		if cat_count != None:
			return cat_count[0]

	def insert_word_to_hisotory_table(self,word,cat):
		cat_no = 0
		if cat == 'possitive':
			cat_no += 1
		if cat == 'negative':
			cat_no += 2
		conn = self.connect_db()
		cursor = conn.cursor()
		sql = 'INSERT INTO history_words (words, cat) VALUES ( "%s", %d)' % \
		(word,cat_no)
		cursor.execute(sql)
		conn.commit()