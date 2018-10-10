from dicmysql import Mysql
from classify import NaiveBayes
import csv
import requests
from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
search = []
with open('train_words.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		search.append(row)
def get_sentence(search):
	x = []
	for a in search:
		x.append(['https://www.google.co.jp/search?q=' +a[0],a[1]] )

	z = []
	for y in x:
		
		html = requests.get(y[0]).content
		soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
		dicriptions = soup.find_all("div", class_="g")
		
		for dicription in dicriptions:

			z.append([dicription.get_text(),y[1]])
	return z

sentences = get_sentence(search)
print(sentences)

#document = 'パワハラ'
#Mysql = NaiveBayes()
#words = Mysql.word_in_cat_probability(document,1)
