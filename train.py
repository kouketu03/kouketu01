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

search = ["ネットドクターズ","ネットドクターズ 退会","ネットドクターズ ログインできない","ネットドクターズ 解約 au","ネットドクターズ 悪質","ネットドクターズ 解約","ネットドクターズ 解約できない","ネットドクターズ 解約方法", "ネットドクターズ 退会できない","ネットドクターズ 登録","ネットドクターズ 評判","ネットドクターズ 評価","ネットドクターズ ポイントサイト"]

#キーワードの検索結果をスクレイピング
def get_sentence(search):
	x = []
	for a in search:
		x.append('https://www.google.co.jp/search?q=' +a )

	z = []
	for y in x:
		
		html = requests.get(y).content
		soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
		dicriptions = soup.find_all("div", class_="g")
		for dicription in dicriptions:
			z.append(dicription.get_text())
	return z

sentences = get_sentence(search)
db = Mysql()
db.fuhyou_insert_sentence(sentences)