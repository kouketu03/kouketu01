/**************************************************/
                  準備
/**************************************************/

STEP1: train_words.csv　に学習用のキーワードを20個準備(一列目はキーワード,二列目はcompany_id)
STEP2: keywords.csv　に施策用のキーワードを入れる (一列目はキーワード,二列目はcompany_id)
STEP3: dicmysql.py にデータベースに接続情報を入れる

/**************************************************/
                  トレーニング
/**************************************************/
STEP3: python train_insert_sentences.py を実行
STEP4: データベースから　sentencesテーブルのcat を振り分ける
STEP5: python train_insert_history_words.py を実行

/**************************************************/
                  施策開始
/**************************************************/
STEP6: python auto-chrome1.py を実行
　　　　　。。。。
