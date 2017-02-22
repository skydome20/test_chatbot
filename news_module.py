# -*- coding: utf8 -*-

#======= parse_news ==========#
import question_module # 問題處理的模組
import re
import time
import requests
from bs4 import BeautifulSoup
import os.path
import jieba # cut word

#======= news_filter ==========#
import jieba.analyse # TF-IDF, textrank : keywords
from collections import Counter

#======= news_analysis ==========#
#import jieba.analyse # TF-IDF, textrank : keywords
from snownlp import SnowNLP # textrank : summary

#======= word2vec ==========#
import logging
from gensim.models import word2vec

#======= demo ==========#
from gensim import models
#====== tfidf ==========#
from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer  
#======= news_similar_filter ==========#
from gensim import corpora, models, similarities





# path: the big table from 'parse_news()'
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# 匯入繁體字庫
jieba.set_dictionary('jieba_dict/dict.txt.big')

# 匯入自訂字庫
jieba.load_userdict("jieba_dict/5w2h.txt")
jieba.load_userdict("jieba_dict/zh_proper_noun.txt")

# 匯入 stopwords 字庫
stopwordset = set()
with open('jieba_dict/stop_words.txt','r',encoding='utf-8') as sw:
	for line in sw:
		stopwordset.add(line.strip('\n'))


# disable INFO message
logger = logging.getLogger('requests_throttler')
logger.addHandler(logging.NullHandler())
logger.propagate = False


#==============================================================================================#
#=================================parse_news===================================================#
#==============================================================================================#
def news_parse(keywords):
    
	"""預備工作 """
	# 瀏覽器型態 為了讓程式像是瀏覽器去訪問網站
	headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
	taiwan_press = {"www.appledaily.com.tw" : "apple", # ok
					"www.chinatimes.com" : "chinatimes", # ok
					"news.ltn.com.tw" : "ltn",  # ok
					"www.storm.mg" : "storm",   # ok
					"www.thenewslens.com" : "thenewslens", # ok
					"www.cna.com.tw" : "cna", #ok
					"udn.com/news" : "udn.news", #ok
					#"www.civilmedia.tw" : "civil", #ok
					"www.businessweekly.com.tw" : "businessweekly" #ok
	}

	keys = list(taiwan_press.keys())    # press url
	vals = list(taiwan_press.values())  # press name


	store_path = "/home/skydome20/Desktop/dbot/dbot.py3/news_folder"


	"""根據關鍵字,網路爬資料"""

	# "google news url" 
	# url = "https://www.google.com.tw/search?tbm=nws&q=川普+site:thenewslens.com"
	url = "https://www.google.com.tw/search?tbm=nws&q="
	#url = url + "+".join(keywords) # 交集
	url = url + "|".join(keywords) # 聯集
	urls = list()
	for news_href in keys:
		urls.append(url + "+site:" + news_href)
    
	#儲存所有新聞標題大表
	title_folder = "/home/skydome20/Desktop/dbot/dbot.py3/news_folder/title/"
	title_output_path = title_folder  + "_".join(keywords) + "title" + ".txt"
	output_title = open(title_output_path, 'w', encoding='utf-8')

	#儲存所有新聞大表
	news_folder = "/home/skydome20/Desktop/dbot/dbot.py3/news_folder/all/"
	news_output_path = news_folder  + "_".join(keywords) + ".txt"
	output_news = open(news_output_path, 'w', encoding='utf-8')

	#儲存所有超連結大表
	href_folder = "/home/skydome20/Desktop/dbot/dbot.py3/news_folder/href/"
	href_output_path = href_folder  + "_".join(keywords) + "_href" + ".txt"
	output_href = open(href_output_path, 'w', encoding='utf-8')

	time.sleep(2)

	for url in urls: # 每間媒體挑20篇新聞
    
		#print(url)
		page = 0 
		while(page < 21): # 20篇新聞
			time.sleep(2)
			query_url = url + "&start=" + str(page)
			# 建立連結 #
			res = requests.get(query_url, headers=headers)
			res.encoding = 'utf-8'
			soup = BeautifulSoup(res.text, "html.parser")

			# 取得新聞的標題和超連結 #
			for news in soup.select("._d7c"):

				time.sleep(1)

				title = news.select("._HId")[0].text # new title
				href = news.find("a")["href"]        # new hyper-link

				# 判斷現在的新聞,是否為新聞清單裡面,可以進行處理的
				now_href = [key for key in keys if key in href]
				if(now_href ==[]): # 如果不在清單裡，就跳到下一則新聞處理
					continue

				# 讀取新聞的超連結
				news_res = requests.get(href, headers=headers)
				news_res.encoding = 'utf-8'
				news_soup = BeautifulSoup(news_res.text, "html.parser")

				# 用新聞標題當儲存文件的名稱
				file_name = title + ".txt"

				# 這篇新聞屬於哪個媒體
				now_press = taiwan_press[now_href[0]] 

				try:

					# 蘋果
					if (now_press == "apple"):
						#content = news_soup.select("#summary")[0].text
						content = news_soup.select(".clearmen")[0].text
						content = news_clean(now_press, content)

					# 自由
					elif (now_press == "ltn"):
						content = news_soup.select("#newstext")[0].text
						content = news_clean(now_press, content)

					# 中時
					elif (now_press == "chinatimes"):
						content = news_soup.select("article")[0].text
						content = news_clean(now_press, content)

					# 聯合新聞網
					elif (now_press == "udn.news"):
						content = news_soup.select("#story_body_content")[0].text
						content = news_clean(now_press, content)

					# 中央通訊社
					elif (now_press == "cna"):
						content = news_soup.select("section")[0].text
						content = news_clean(now_press, content)

					# 關鍵評論網
					elif (now_press == "thenewslens"):
						content = news_soup.select(".article-content")[0].text
						content = news_clean(now_press, content)

					# 風傳媒
					elif (now_press == "storm"):
						content = news_soup.select("article")[0].text
						content = news_clean(now_press, content)
                    
					# 商業週刊
					elif (now_press == "businessweekly"):
						content = news_soup.select(".be-changed")[0].text
						content = news_clean(now_press, content)

					# 公民行動
					elif (now_press == "civil"):
						content = news_soup.select(".clearfix")[0].text

						path = store_path + "/civil/" + file_name

					# news filter for match-problem news
					check_idx = False
					TFIDF_keywords = jieba.analyse.extract_tags(content, topK=5, withWeight=False)
					TEXTRANK_keywords = jieba.analyse.textrank(content, topK=5, withWeight=False)
					for keyword in keywords:
						if keyword in TFIDF_keywords  : 
							check_idx = True
						if keyword in TEXTRANK_keywords  : 
							check_idx = True

					if check_idx == False:
						continue

					# 新聞大表
					output_title.write(title + "\n")
					output_news.write(content + "\n")
					output_href.write(href + "\n")		

				except:
					aaa = 10

			page += 10
			#print('...Parsing...')

	# 新聞大表
	output_news.close()
	output_href.close()
	#print("大表路徑:" + news_output_path)
	return( (title_output_path, news_output_path, href_output_path))


#==============================================================================================#
#================================= news_analysis ==============================================#
#==============================================================================================#
def news_summary(title_path, news_path, href_path):
	textnum = 0

	# 新聞標題
	f = open(title_path, 'r', encoding='utf-8')
	title_table = f.readlines()
	f.close()

	# 新聞超連結
	f = open(href_path, 'r', encoding='utf-8')
	href_table = f.readlines()
	f.close()


	print("(新聞標題※摘要※超連結)" + "\n")
	time.sleep(2)

	with open(news_path,'r',encoding='utf-8') as content :
		for text in content:
            
			news_title = title_table[textnum]
			news_href = href_table[textnum]

			print ( "【" + news_title.rstrip() + "】" + "\n" + 
					"(1)" + SnowNLP(text).summary(5)[0] + "\n" + 
					"(2)" + SnowNLP(text).summary(5)[1] + "\n" + 
					"(3)" + SnowNLP(text).summary(5)[2] + "\n" + 
					#"(4)" + SnowNLP(text).summary(5)[3] + "\n" + 
					#"(5)" + SnowNLP(text).summary(5)[4] + "\n" + 
					news_href)
			#break
			#TFIDF_words = jieba.analyse.extract_tags(text, topK=5, withWeight=False) 
			#print("TF-IDF:" , TFIDF_words)

			#textrank_words = jieba.analyse.textrank(text, topK=5, withWeight=False) 
			#print("TextRank:" , textrank_words)
			textnum += 1
			if textnum == 5 : break



#==============================================================================================#
#================================= news_cut====================================================#
#==============================================================================================#
def news_cut(path) :
	# 標點符號
	symbol_list = u''':!),.:;?]}¢'"、。#/\><〉$》」』】〕〗〞︰︱︳﹐､﹒
﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝╱︴︶︸︺︼︾﹀﹂﹄﹏､～￠
々‖•·ˇˉ―--′’”([{£¥'"‵／〈《「『【〔〖（［｛￡￥〝︵︷︹︻
︽︿﹁﹃﹙﹛﹝（｛“‘-—_…'''

	# 切字後的結果匯出
	output_path = '/home/skydome20/Desktop/test.txt'
	output = open(output_path, 'w', encoding='utf-8')
	texts_num = 0
    
	with open(path,'r') as content :
		for line in content:
			words = jieba.cut(line, cut_all=False)
			for word in words:
				if word not in stopwordset:     # stop words
					if word not in symbol_list: # symbol remove
						output.write(word +' ')
			texts_num += 1
			output.write('\n')
			#if texts_num % 10 == 0:
				#logging.info("已完成前 %d 行的斷詞" % texts_num)
                
	output.close()


#==============================================================================================#
#================================= news_filter(TF-IDF)==================================#
#==============================================================================================#

## use cut-articles

def news_associated_keywords(keywords, news_path):
	jieba.analyse.set_stop_words("jieba_dict/stop_words.txt")
	textnum = 0
	TFIDF_keywords = tfidf_top_words(news_path, topk=5)
    
	TEXTRANK_keywords = []
	with open(news_path,'r',encoding='utf-8') as content :
		for text in content:
			TEXTRANK_keywords.extend(jieba.analyse.textrank(text, topK=5, withWeight=False))
			textnum += 1
			#TFIDF_keywords.extend(jieba.analyse.extract_tags(text, topK=15, withWeight=False) )

	print("The number of news is :" + textnum)
            
	all_keywords = TFIDF_keywords + TEXTRANK_keywords
	associated_keywords = list()
	top10_assoicated_words = Counter(all_keywords).most_common(10)
	print(top10_assoicated_words)
	for key, val in top10_assoicated_words:
		if key not in keywords and val > 1:   
			associated_keywords.append(key)
            
	if len(associated_keywords) > 5:     
		return associated_keywords[0:5]  
	else: 
		return(associated_keywords)

#==============================================================================================#
#================================= news_word2vec===============================================#
#==============================================================================================#
def news_word2vec(path):
	# path: the big table after cutting, from 'news_cut()'
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

	# 讀取該問題所有新聞的大表(經過切字)，製作詞向量

	# sentences = [['first', 'sentence'], ['second', 'sentence']]
	# we have to transfer the txt file to the format above
	sentences = list()
	news_bigTable = open(path, 'r', encoding='utf-8')
	content = news_bigTable.readlines()
	for line in content:
		tmp = line.split(' ')
		tmp = [elm for elm in tmp if elm != '']
		sentences.append(tmp)

	# 訓練詞向量
	model = word2vec.Word2Vec(sentences, 
							  size=20,       # dimensiton
							  alpha = 0.025,  # learning rate -> to min alpha (default = 0.025)
							  sg = 1,         # 1:skip-gram; 0:cbow (default = 0)
							  window = 20,    # recommend = 5
							  workers = 4,    # running threads (default = 3)
							  min_count = 5   # a word will not be regarded as the trainning target if the frequency < min_count 
	)

	model.save_word2vec_format(u"news_article_word2vector_20_skipgram20_model.txt", binary=False)
	return(model)


#==============================================================================================#
#================================= news_demo ==================================================#
#==============================================================================================#
def demo(word2vec_model):
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

	#directory = "word_vector_set/"
	#word2vec_model = directory + "wiki_article_word2vector_300_skipgram5_model.bin"
	#word2vec_model = u"news_article_word2vector_20_skipgram20_model.txt"

	#model = models.Word2Vec.load_word2vec_format(word2vec_model, binary=False)
	#model.save_word2vec_format('path/to/GoogleNews-vectors-negative300.txt', binary=False)

	model = word2vec_model
	print("提供 3 種測試模式\n")
	print("輸入一個詞，則去尋找前一百個該詞的相似詞")
	print("輸入兩個詞，則去計算兩個詞的餘弦相似度")
	print("輸入三個詞，進行類比推理")

	while True:
		try:
			query = input()
			q_list = query.split()

			if query == "exit":
				break

			# 尋找前一百個該詞的相似詞
			elif len(q_list) == 1:
				print("相似詞前 100 排序")
				res = model.most_similar(q_list[0],topn = 20)
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
				res = model.most_similar(positive = [q_list[0], q_list[2]],
										 negative = [q_list[1]], 
										 topn= 20)
				for item in res:
					print(item[0] + "," + str(item[1]) )

			print("----------------------------")

		except Exception as e:
			print(repr(e))

#==============================================================================================#
#================================= news_clean =================================================#
#==============================================================================================#
def news_clean(press, content):
	clean_content = content
	if press == 'apple':
		split_contents = clean_content.splitlines()
		clean_content = max(split_contents, key=len)
		clean_content = re.sub(r"\（.*?\）", '', clean_content) 
		clean_content = re.sub(r"\(.*?\)", '', clean_content) 
		clean_content = re.sub(r"\〔.*?\〕", '', clean_content)  
		clean_content = re.sub(r"\【.*?\】", '', clean_content) 
		clean_content = re.sub(r"googletag.cmd.push\(.*?\}\)", '', clean_content)
		clean_content = re.sub("來稿請寄onlineopinions@appledaily.com.tw，文長以500字為度，一經錄用，將發布在蘋果日報即時新聞區，唯不付稿酬。請勿一稿兩投，本報有刪改權，當天未見報，請另行處理，不另退件或通知。", '', clean_content)
		clean_content = re.sub("《蘋果日報即時新聞》新闢《即時論壇》，歡迎讀者投稿，對新聞時事表達意見。", '', clean_content)
		clean_content = re.sub("你對新聞是否不吐不快？", '', clean_content)

       
	elif press == 'ltn':
		split_contents = clean_content.splitlines()
		clean_content = max(split_contents, key=len)
		clean_content = re.sub(r"\（.*?\）", '', clean_content) 
		clean_content = re.sub(r"\(.*?\)", '', clean_content) 
		clean_content = re.sub(r"\〔.*?\〕", '', clean_content)  
		clean_content = re.sub(r"\【.*?\】", '', clean_content)       

	elif press == 'chinatimes':
		split_contents = clean_content.splitlines()
		clean_content = max(split_contents, key=len)
		clean_content = re.sub(r"\（.*?\）", '', clean_content) 
		clean_content = re.sub(r"\(.*?\)", '', clean_content) 
		clean_content = re.sub(r"\〔.*?\〕", '', clean_content)  
		clean_content = re.sub(r"\【.*?\】", '', clean_content) 
  
	elif press == 'udn.news':
		clean_content = re.sub(r"\（.*?\）", '', clean_content) 
		clean_content = re.sub(r"\(.*?\)", '', clean_content) 
		clean_content = re.sub(r"\〔.*?\〕", '', clean_content)  
		clean_content = re.sub(r"\【.*?\】", '', clean_content) 
		clean_content = re.sub(r".*function.*\}", '', clean_content)
		clean_content = re.sub(r"分享   facebook", '', clean_content) 
		clean_content = re.sub(r"美聯社", '', clean_content)  
		clean_content = re.sub(r"圖／", '', clean_content) 
		clean_content = re.sub(r"圖擷自", '', clean_content)  
    
	elif press == 'cna':
		split_contents = clean_content.splitlines()
		clean_content = max(split_contents, key=len)
		clean_content = re.sub(r"\（.*?\）", '', clean_content) 
		clean_content = re.sub(r"\(.*?\)", '', clean_content) 
		clean_content = re.sub(r"\〔.*?\〕", '', clean_content)  
		clean_content = re.sub(r"\【.*?\】", '', clean_content) 
		clean_content = re.sub(r"1060.*", '', clean_content) 
        
	elif press == 'thenewslens':
		clean_content = re.sub(r"googletag.*", '', clean_content) 
		clean_content = re.sub(r"var.*", '', clean_content) 
		clean_content = re.sub(r".defineSlot.*", '', clean_content)  
		clean_content = re.sub(r".addService.*", '', clean_content) 
		clean_content = re.sub(r"\}\);", '', clean_content)         
		clean_content = re.sub(r"延伸閱讀：.*", '', clean_content)
		clean_content = re.sub(r"\（.*?\）", '', clean_content) 
		clean_content = re.sub(r"\(.*?\)", '', clean_content) 
		clean_content = re.sub(r"\〔.*?\〕", '', clean_content)  
		clean_content = re.sub(r"\【.*?\】", '', clean_content) 
		clean_content = clean_content.replace("\n", "")
		clean_content = clean_content.replace(" ", "")
        
	elif press == 'storm': 
		clean_content = re.sub(r"\（.*?\）", '', clean_content) 
		clean_content = re.sub(r"\(.*?\)", '', clean_content) 
		clean_content = re.sub(r"\〔.*?\〕", '', clean_content)  
		clean_content = re.sub(r"\【.*?\】", '', clean_content) 
		clean_content = re.sub(r"[A-Za-z0-9]*", '', clean_content)
		clean_content = clean_content.replace(" ", "")
		clean_content = clean_content.replace("\n", "")
		clean_content = re.sub(r"[\.\{\;\)\}\#\/\—\'\,\@\-\&\:\[\]]*", '', clean_content)
		clean_content = clean_content.replace("\t", "")
		clean_content = clean_content.replace("年月日", "")
		clean_content = clean_content.replace("\r", "")
		clean_content = clean_content.replace(" ", "")
		clean_content = clean_content.replace("\’", "")
        
        
	elif press == "businessweekly": 
		clean_content = clean_content.replace("\n", "")
		clean_content = re.sub(r"資料整理：.*", '', clean_content)
        
	return(clean_content)

	return(content)


#==============================================================================================#
#================================= news_similar_filter=========================================#
#==============================================================================================#

def news_similar_filter(path):
	path = '/home/skydome20/Desktop/test.txt'
	docs = list()
	with open(path,'r',encoding='utf-8') as doc_set:
		for doc in doc_set:
			docs.append(doc)

	# doc to words
	texts = [[word for word in doc.split()] for doc in docs]

	# bag-of-words 
	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]

	# TF-IDF 
	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]

	# LSI model
	lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10)

	# create index of LSI
	index = similarities.MatrixSimilarity(lsi[corpus])

	# check similar docs ind
	num_doc = len(index)
	keep_docs = list(range((num_doc)))
	ind = 0
	# check each doc which is similar to the others
	for i in index:
		if ind >= num_doc:
			break
		else:
			m = list(i)
			# simlar_doc
			simlar_docs = [index for index,value in enumerate(m) if value > 0.75 and index > ind]
			# remove simlar_doc ind
			for elem in simlar_docs:
				if elem in keep_docs:
					keep_docs.remove(elem)
			ind += 1
            
	# remove simlar_doc and write back to original files     
	docs = list()
	with open(path,'r',encoding='utf-8') as doc_set:
		for doc in doc_set:
			docs.append(doc)

	f = open(path, "w")
	for ind in keep_docs:  
		f.write(docs[ind])
	f.close()
            
#==============================================================================================#
#================================= keywords_tabo===============================================#
#==============================================================================================#
def keywords_tabo(keywords):
	tabo_words = keywords
	tmp = list()
	for word in keywords:
		tmp.extend( list(jieba.cut_for_search(word)) )
   
	tabo_words.extend(tmp)
	return(tabo_words)

#==============================================================================================#
#================================= tfidf ======================================================#
#==============================================================================================#
def tfidf_top_words(news_path, topk=5):
	news_cut(news_path)
	path = "/home/skydome20/Desktop/test.txt"

	# read files

	corpus = []
	with open(path,'r',encoding='utf-8') as doc_set:
		for doc in doc_set:
			corpus.append(doc)

	vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频  
	transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值  
	tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵  

	word=vectorizer.get_feature_names()#获取词袋模型中的所有词语  
	weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重 
	total_words = [] 
	for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重

		#print (u"-------这里输出第" + str(i) + u"类文本的词语tf-idf权重------"  )
		d = dict()
		for j in range(len(word)):  
			if weight[i][j] != 0:
				d.update({word[j] : weight[i][j]})
		# sort words by weights
		lst = list()
		for (key,val) in d.items():
			lst.append( (val,key) )
		lst.sort(reverse=True)


		# top k words 
		top_words = []
		counter = 0
		for (val, key) in lst:
			if counter >= topk:
				break
			top_words.append(key)
			counter +=1


		for e in top_words:
			total_words.append(e)


	return(total_words)

if __name__ == '__main__':


	print('this is main function')





