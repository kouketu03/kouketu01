import csv
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from threading import Timer
from bs4 import BeautifulSoup
from classify import NaiveBayes
from dicmysql import Mysql
d = DesiredCapabilities.CHROME
d['loggingPrefs'] = { 'browser':'ALL' }
classify = NaiveBayes()
Mysql = Mysql()

def auto_Firefox():
	driver = webdriver.Firefox()
	driver.get("https://www.google.co.jp/")
	with open('positive-keywords.csv','r') as f:
		reader = csv.reader(f)
		for row in reader:
			driver.find_element_by_id("lst-ib").clear() 
			driver.find_element_by_id("lst-ib").send_keys(row[0])
			time.sleep(1)
			driver.find_element_by_id("lst-ib").click()
			related_words = driver.find_elements_by_class_name("sbqs_c")
			i = -1
			for related_word in related_words:
				i +=1
				#ページはjsにリフレッシュされたため、もう一回要素取得しないといけない。
				#参考：https://www.cnblogs.com/fengpingfan/p/4583325.html
				if i > 0:
					driver.find_element_by_id("lst-ib").clear()
					driver.find_element_by_id("lst-ib").send_keys(row[0])
					time.sleep(1)
					driver.find_element_by_id("lst-ib").click()
				related_words02 = driver.find_elements_by_class_name("sbqs_c")
				rel_word = related_words02[i].text
				check = Mysql.check_history_word(rel_word,row[1])
				print( rel_word + ':' + str(check))
				if check == 'nothing' and related_word != '':
					cat = classify.word_classify(rel_word,row[1])
					Mysql.insert_word_to_hisotory_table(rel_word,,row[1],cat)
				if check == 2 : continue
				if check == 1 :
					related_words02[i].click()
					print( rel_word +'clicked')
					time.sleep(2)
					#前のページに戻らないと今のページ内の関連ワードをクリック続けるようになってしまいます。
					driver.back()
					print( 'back')
					time.sleep(2)
			time.sleep(1)
	driver.quit()
	t=threading.Timer(1,auto_Firefox)
	t.start()

if __name__=='__main__':
    t=threading.Thread(target=auto_Firefox)
    t.start()