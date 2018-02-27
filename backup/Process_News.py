from gensim import corpora, models, similarities

def cut(path):
	# 標點符號
	symbol_list = u''':!),.:;?]}¢'"、。#/\><〉$》」』】〕〗〞︰︱︳﹐､﹒
﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝╱︴︶︸︺︼︾﹀﹂﹄﹏､～￠
々‖•·ˇˉ―--′’”([{£¥'"‵／〈《「『【〔〖（［｛￡￥〝︵︷︹︻
︽︿﹁﹃﹙﹛﹝（｛“‘-—_…'''

	# 切字後的結果匯出
	output_path = '/home/skydome20/Desktop/dbot/dbot.py3/news_folder/cut/cut.txt' 
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
			if texts_num % 10 == 0:
				logging.info("已完成前 %d 行的斷詞" % texts_num)
                
	output.close()
	return (output_path)






#==============================================================================================#
#================================= news_similar_filter=========================================#
#==============================================================================================#

def news_similar_filter(path):

	docs = list()
	with open(path,'r',encoding='utf-8') as doc_set:
		for doc in doc_set:
			docs.append(doc)
	print("The original news: " + str(len(docs)) )
	# doc to words
	texts = [[word for word in doc.split()] for doc in docs]

	# bag-of-words 
	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]

	# TF-IDF 
	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]

	# LSI model(=LSA)
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
			simlar_docs = [index for index,value in enumerate(m) if value > 0.9 and index > ind]
			# remove simlar_doc ind
			for elem in simlar_docs:
				if elem in keep_docs:
					keep_docs.remove(elem)
			ind += 1
            
	# remove similar_doc and write back to original files     
	docs = list()
	hrefs = list()
	titles = list()
	t_path = "/home/skydome20/Desktop/news_folder/title/台大_論文造假_title.txt"
	n_path = "/home/skydome20/Desktop/news_folder/all/台大_論文造假.txt"
	h_path = "/home/skydome20/Desktop/news_folder/href/台大_論文造假_href.txt"
	tt_path = "/home/skydome20/Desktop/news_folder_filter/title/台大_論文造假_title.txt"
	nn_path = "/home/skydome20/Desktop/news_folder_filter/all/台大_論文造假.txt"
	hh_path = "/home/skydome20/Desktop/news_folder_filter/href/台大_論文造假_href.txt"

	#update titles
	with open(t_path,'r',encoding='utf-8') as doc_set:
		for doc in doc_set:
			titles.append(doc)
	f = open(tt_path, "w")
	for ind in keep_docs:  
		f.write(titles[ind])
	f.close()
    
	#update hrefs
	with open(h_path,'r',encoding='utf-8') as doc_set:
		for doc in doc_set:
			hrefs.append(doc)
	f = open(hh_path, "w")
	for ind in keep_docs:  
		f.write(hrefs[ind])
	f.close()
    
	#update news  
	with open(n_path,'r',encoding='utf-8') as doc_set:
		for doc in doc_set:
			docs.append(doc)
	print("The keep news: " + str(len(keep_docs)) )
	print("The keep news =" , keep_docs)
	f = open(nn_path, "w")
	for ind in keep_docs:  
		f.write(docs[ind])
	f.close()

    
    
	return(path)
