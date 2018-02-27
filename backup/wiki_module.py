# -*- coding: utf-8 -*-

#=======article_extract==========#
import logging
import sys
from gensim.corpora.wikicorpus import WikiCorpus

#=======article_cut==============#
import jieba
#import logging

#=======article_word2vec=========#
from gensim.models import word2vec
#import logging
import time

#=======article_demo=============#
#from gensim.models import word2vec
from gensim import models
#import logging


#==============================================================================================#
#=================================wiki_article_cut=============================================#
#==============================================================================================#
def wiki_article_extract():
	directroy = "/home/skydome20/Desktop/dbot/dbot.py3/wiki_article/"
	wiki_zip_name = directroy + "zhwiki-20161020-pages-articles.xml.bz2"
#
#
#    if len(sys.argv) != 2:
#        print("Usage: python3 " + sys.argv[0] + " wiki_data_path")
#        exit()
#
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	wiki_corpus = WikiCorpus(wiki_zip_name, dictionary={}, lemmatize=False)

	texts_num = 0
    
	# 將wiki提供的資料（2016/10/20）長度大於50的整理在一個txt中 用換行符號\n區隔
	# 再進行簡體字轉繁體字
	# 再用jieba切字
	with open("wiki_texts.txt",'w',encoding='utf-8') as output:
		for text in wiki_corpus.get_texts():
			output.write(b' '.join(text).decode('utf-8') + '\n')
			texts_num += 1
			if texts_num % 10000 == 0:
				logging.info("已處理 %d 篇文章" % texts_num)


#==============================================================================================#
#=================================wiki_article_cut=============================================#
#==============================================================================================#
# 簡體字轉繁體字後 （指令：opencc -i wiki_texts.txt -o wiki_zh_tw.txt ）
# 用jieba切字

def wiki_article_cut():
	directroy = "/home/skydome20/Desktop/dbot/dbot.py3/wiki_article/"
	wiki_text_name = directroy + 'wiki_zh_tw.txt'

	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

	# 匯入繁體字庫
	jieba.set_dictionary('jieba_dict/dict.txt.big')

	# 匯入自訂字庫
	jieba.load_userdict("jieba_dict/5w2h.txt")
	jieba.load_userdict("jieba_dict/zh_proper_noun.txt")


	# load stopwords set
	stopwordset = set()
	with open('jieba_dict/stop_words.txt','r',encoding='utf-8') as sw:
		for line in sw:
			stopwordset.add(line.strip('\n'))


	wiki_seg_name = directroy + "wiki_seg.txt"
	output = open(wiki_seg_name,'w')
    
	texts_num = 0
    
	with open(wiki_text_name,'r') as content :
		for line in content:
			words = jieba.cut(line, cut_all=False)
			for word in words:
				if word not in stopwordset:
					output.write(word +' ')
			texts_num += 1
			if texts_num % 10000 == 0:
				logging.info("已完成前 %d 行的斷詞" % texts_num)
	output.close()


#==============================================================================================#
#=================================wiki_article_word2vec========================================#
#==============================================================================================#
def wiki_article_word2vector():

	#time.sleep(36000)
	
	print("i")

	directroy = "/home/skydome20/Desktop/dbot/dbot.py3/wiki_article/"
	wiki_seg_name = directroy + "wiki_seg.txt"

	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
	sentences = word2vec.Text8Corpus(wiki_seg_name)
	#print(sentences)

	
	# 訓練詞向量
	model = word2vec.Word2Vec(sentences, 
							  size=250,         # dimensiton
							  alpha = 0.025,   # learning rate -> to min alpha (default = 0.025)
							  sg = 1,          # 1:skip-gram; 0:cbow (default = 0)
							  window = 8,      # recommend = 5
							  workers = 4,     # running threads (default = 3)
							  min_count = 5   # a word will not be regarded as the trainning target if the frequency < min_count 
	)


	model.save_word2vec_format(u"/home/skydome20/Desktop/dbot/dbot.py3/wiki_word2vec_set/wiki_article_word2vector_200_skipgram8_model.bin", binary=True)

    # how to load a model ?
    # model = word2vec.Word2Vec.load_word2vec_format("your_model.bin", binary=True)



#==============================================================================================#
#=================================wiki_article_demo========================================#
#==============================================================================================#

def wiki_article_demo(path):
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

	model = models.Word2Vec.load_word2vec_format(path, binary=True)


	print("提供 3 種測試模式\n")
	print("輸入一個詞，則去尋找前一百個該詞的相似詞")
	print("輸入兩個詞，則去計算兩個詞的餘弦相似度")
	print("輸入三個詞，進行類比推理")
    

	print("%s之於%s，如%s之於" % ("法國","巴黎","英國"))
	res = model.most_similar(positive = ["法國","英國"], negative =  ["巴黎"], topn= 20)
	for item in res:
		print(item[0]+","+str(item[1]))
"""      
	while True:
		try:
			query = input()
			q_list = query.split()

			if query == "exit":
				break

			# 尋找前一百個該詞的相似詞
			elif len(q_list) == 1:
				print("相似詞前 100 排序")
				res = model.most_similar(q_list[0],topn = 30)
				for item in res:
					print(item[0] + "," + str(item[1]) )

			#計算兩個詞的餘弦相似度
			elif len(q_list) == 2:
				print("計算 Cosine 相似度")
				res = model.similarity(q_list[0], q_list[1])
				print(res)

			#類比推理: analylog
			else:
				print("%s之於%s，如%s之於" % (q_list[0],q_list[1],q_list[2]))
				res = model.most_similar(positive = [q_list[0],q_list[2]],
										 negative =  [q_list[1]], 
										 topn= 20)
				for item in res:
					print(item[0]+","+str(item[1]))

			print("----------------------------")


		except Exception as e:
			print(repr(e))
"""

if __name__ == "__main__":
	#wiki_article_extract()
	#wiki_article_cut()
	#wiki_article_word2vector()
	wiki_article_demo()





