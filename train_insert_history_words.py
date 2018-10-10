import csv
from classify import NaiveBayes
from dicmysql import Mysql
classify = NaiveBayes()
Mysql = Mysql()

def train_insert_history_words():
	with open('train_words.csv','r') as f:
		reader = csv.reader(f)
		for row in reader:
			check = Mysql.check_history_word(row[0])
			print( x + ':' + str(check))
			if check == 'nothing' and check != '':
				print('Classify the ' + row[0] )
				cat = classify.word_classify(row[0])
				print('Classify finished')
				print('Insert "'+ row[0] +'"" to hisotory_table')
				Mysql.insert_word_to_hisotory_table(row[0],row[1],cat)
				print('Insert "'+ row[0] +'"" to hisotory_table finished')
			if check == 2 : continue
			if check == 1 : continue

if __name__=='__main__':
	print('Insert the words into database')
	train_insert_history_words()
	print('Insert finished')