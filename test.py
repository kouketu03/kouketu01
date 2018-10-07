from dicmysql import Mysql
from classify import NaiveBayes

document = '美人計画　ログインできない'
Mysql = NaiveBayes()
words = Mysql.word_in_cat_probability(document,2)
print(words)