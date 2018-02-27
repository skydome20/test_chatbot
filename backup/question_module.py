# -*- coding: utf8 -*-
import requests
from bs4 import BeautifulSoup
import jieba # cut word
import os.path
import re

# 繁體字庫下載
TC_dict = 'dict.txt.big'
if os.path.isfile(TC_dict) == False :
	import requests
	url = 'https://raw.githubusercontent.com/fxsjy/jieba/master/extra_dict/dict.txt.big'
	r = requests.get(url)
	open(TC_dict, 'wb').write(r.content)

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
        
        
        
# 切字模組： 去除標點符號，空白符號，下底線
def cut(question):

	# 問題字串處理   
	question = re.sub(r"[^\w]", "", question)  # 去除（標點）符號
	question = question.strip()                # 去除空白符號
	question = question.replace("_", "")       # 去除下底線
	cut_question = list(jieba.cut(question, cut_all=False)) # 切字
	question_keywords = list() 
	
	for word in cut_question:
		if word not in stopwordset:     # stop words
			question_keywords.append(word)

	return(question_keywords) # return chinese keywords 



# 錯字模組：利用google修正錯字
def typo_correction(question):
	try:
		# 瀏覽器型態，讓程式模擬成瀏覽器
		headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

		# google 搜尋
		url = "https://www.google.com.tw/search?q="
		query_url = url + question

		res = requests.get(query_url, headers=headers)
		res.encoding = 'utf-8'
		soup = BeautifulSoup(res.text, "html.parser")

		# 錯字校正
		corrected_str = soup.select(".spell")[1].text

		if(corrected_str == ""):
			return(question)
		else:
			#print("原始問題：" + question)
			return(corrected_str)
	except:
		return(question)


def handler(question):

	typo_free_question = typo_correction(question) # 問題錯字處理
	#print(typo_free_question)
	tokens = cut(typo_free_question)    # 問題切字處理
	#print(tokens)
	return(tokens)
	


# executed as script, do something
if __name__ == '__main__':
    print ( handler(question) )




