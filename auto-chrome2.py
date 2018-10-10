import csv
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from threading import Timer
from classify import NaiveBayes
from dicmysql import Mysql
d = DesiredCapabilities.CHROME
d['loggingPrefs'] = { 'browser':'ALL' }
classify = NaiveBayes()
Mysql = Mysql()


def auto_chrome():
	with open('keywords.csv','r') as f:
		reader = csv.reader(f)
		for row in reader:
			driver = webdriver.Chrome("C:/Users/kou-k/AppData/Local/driver/chromedriver.exe",desired_capabilities=d)
			driver.get("https://www.google.co.jp/")
			driver.find_element_by_id("lst-ib").clear()
			check = Mysql.check_history_word(row[0],row[1])
			print( x + ':' + str(check))
			if check == 'nothing' :
				cat = classify.word_classify(row[0],row[1])
				Mysql.insert_word_to_hisotory_table(row[0],row[1],cat)
			if check == 2 : continue
			if check == 1 :
				driver.find_element_by_id("lst-ib").send_keys(row[0])
				driver.find_element_by_id("lst-ib").send_keys(Keys.ENTER)
				print( driver.title)
			time.sleep(1)
			driver.quit()
	t=threading.Timer(1,auto_chrome)
	t.start()

if __name__=='__main__':
    t=threading.Thread(target=auto_chrome)
    t.start()