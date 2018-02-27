#======= associated_keywords ==========#
import jieba.analyse # TF-IDF, textrank : keywords
from collections import Counter

#======= summary ==========#
import jieba.analyse # TF-IDF, textrank : keywords
from snownlp import SnowNLP # textrank : summary

#====== tfidf ==========#
from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer  

#======= word2vec ==========#
import logging
from gensim.models import word2vec


## use cut-articles

def associated_keywords(keywords, news_path):
	jieba.analyse.set_stop_words("jieba_dict/stop_words.txt")
	textnum = 0
	TFIDF_keywords = tfidf_top_words(news_path, topk=5)
    
	TEXTRANK_keywords = []
	with open(news_path,'r',encoding='utf-8') as content :
		for text in content:
			TEXTRANK_keywords.extend(jieba.analyse.textrank(text, topK=5, withWeight=False))
			textnum += 1
			#TFIDF_keywords.extend(jieba.analyse.extract_tags(text, topK=15, withWeight=False) )

	print("The number of news is :" + str(textnum))
            
	all_keywords = TFIDF_keywords + TEXTRANK_keywords
	associated_keywords = list()
	top10_assoicated_words = Counter(all_keywords).most_common(15)
	#print(top10_assoicated_words)
    
	associated_keywords = [tuple_keywords for tuple_keywords in top10_assoicated_words if tuple_keywords[0] not in keywords]   
	print(associated_keywords)
	return_keywords = list()
	if len(associated_keywords) > 10:    
		top_weight = associated_keywords[4][1] # top 5
		for key, val in associated_keywords:
			if val >= top_weight:
				return_keywords.append(key)

	else: 
		for key, val in associated_keywords:
			return_keywords.append(key)
            
	return(return_keywords)



#==============================================================================================#
#================================= news_analysis(summary, sementiment)=========================#
#==============================================================================================#
def summary(title_path, news_path, href_path):
	textnum = 0
	top5_ind = 0
	# 新聞標題
	f = open(title_path, 'r', encoding='utf-8')
	title_table = f.readlines()
	f.close()

	# 新聞超連結
	f = open(href_path, 'r', encoding='utf-8')
	href_table = f.readlines()
	f.close()


	#print("(新聞標題※摘要※超連結)" + "\n")
	time.sleep(2)
	print ( "Positive Articles" + "\n" )
	with open(news_path,'r',encoding='utf-8') as content :
		for text in content:
			news_title = title_table[textnum]
			news_href = href_table[textnum]
			snownlp_text = SnowNLP(text)
			#Positive/Negative value + textRank summary
			if snownlp_text.sentiments > 0.9:
				print ( "【" + news_title.rstrip() + "】 " , end="")
				print (snownlp_text.sentiments)
				for iii in list(range(1,6)):
					print ("---" + snownlp_text.summary(5)[(iii-1)] )
				print (news_href)
				top5_ind += 1
            
			"""
			# use textRank summary to calculate P/N value 
			pn_value = (SnowNLP(snownlp_text.summary(1)[0]).sentiments)             
			if pn_value < 0.1:
				print ( "【" + news_title.rstrip() + "】 " , end="")
				print (pn_value)
				print("***" + snownlp_text.summary(1)[0] )
				for iii in list(range(1,6)):
					print ("---" + snownlp_text.summary(5)[(iii-1)] )
				print (news_href)
				top5_ind += 1
			"""



            
            
			#break
			#TFIDF_words = jieba.analyse.extract_tags(text, topK=5, withWeight=False) 
			#print("TF-IDF:" , TFIDF_words)

			#textrank_words = jieba.analyse.textrank(text, topK=5, withWeight=False) 
			#print("TextRank:" , textrank_words)
			textnum += 1
			if top5_ind == 10 : break


#==============================================================================================#
#================================= tfidf ======================================================#
#==============================================================================================#
def tfidf_top_words(path, topk=5):

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

#==============================================================================================#
#================================= news_word2vec===============================================#
#==============================================================================================#
def word2vec(path):
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
def word2vec_demo(word2vec_model):
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
#================================= keywords_tabu===============================================#
#==============================================================================================#
def keywords_tabu(keywords):
	tabu_words = keywords
	tmp = list()
	for word in keywords:
		tmp.extend( list(jieba.cut_for_search(word)) )
   
	tabu_words.extend(tmp)
	return(tabu_words)
