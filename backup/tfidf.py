from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer  
import news_module
#news_path = "/home/skydome20/Desktop/dbot/dbot.py3/news_folder/all/客運_致死.txt"

def tfidf_top_words(news_path, topk=5):
	news_module.news_cut(news_path)
	path = "/home/skydome20/Desktop/test.txt"
	k = 3
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
			if counter >= k:
				break
			top_words.append(key)
			counter +=1


		for e in top_words:
			total_words.append(e)


	return(total_words)



