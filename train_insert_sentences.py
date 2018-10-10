# coding:utf-8 
import io  
import sys
import csv
import requests
from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
from janome.tokenizer import Tokenizer
from dicmysql import Mysql
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

search = []

with open('train_words.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		search.append(x)
print(search)
#キーワードの検索結果をスクレイピング
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

print('Insert the words into database')
sentences = get_sentence(search)
db = Mysql()
db.fuhyou_insert_sentence(sentences)
print('Insert finished')