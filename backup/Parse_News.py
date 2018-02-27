# -*- coding: utf8 -*-

#======= parse_news ==========#
import question_module # 問題處理的模組
import re
import time
import requests
from bs4 import BeautifulSoup
import os.path
import jieba # cut word
import logging
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
def parse(keywords, intersect_or_union, num_of_news):
    
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
					"www.civilmedia.tw" : "civil", #ok
					"www.businessweekly.com.tw" : "businessweekly" #ok
	}

	keys = list(taiwan_press.keys())    # press url
	vals = list(taiwan_press.values())  # press name


	store_path = "/home/skydome20/Desktop/dbot/dbot.py3/news_folder"


	"""根據關鍵字,網路爬資料"""

	# "google news url" 
	# url = "https://www.google.com.tw/search?tbm=nws&q=allintext:川普+site:thenewslens.com"
	url = "https://www.google.com.tw/search?tbm=nws&q=allintext:"
	url = url + intersect_or_union.join(keywords) 
	urls = list()
	for news_href in keys:
		urls.append(url + "+site:" + news_href)
    
	#儲存所有新聞標題大表
	title_folder = "/home/skydome20/Desktop/dbot/dbot.py3/news_folder/title/"
	title_output_path = title_folder  + "_".join(keywords) + "_title" + ".txt"
	output_title = open(title_output_path, 'w', encoding='utf-8')

	#儲存所有新聞大表
	news_folder = "/home/skydome20/Desktop/dbot/dbot.py3/news_folder/all/"
	news_output_path = news_folder  + "_".join(keywords) + ".txt"
	output_news = open(news_output_path, 'w', encoding='utf-8')

	#儲存所有超連結大表
	href_folder = "/home/skydome20/Desktop/dbot/dbot.py3/news_folder/href/"
	href_output_path = href_folder  + "_".join(keywords) + "_href" + ".txt"
	output_href = open(href_output_path, 'w', encoding='utf-8')

	for url in urls: # 每間媒體挑20篇新聞
    
		print(url)
		page = 0 
		while(page < (num_of_news + 1)): # 50篇新聞
			time.sleep(2)
			query_url = url + "&start=" + str(page)
			# 建立連結 #
			res = requests.get(query_url, headers=headers)
			res.encoding = 'utf-8'
			soup = BeautifulSoup(res.text, "html.parser")

			# 取得新聞的標題和超連結 #
			for news in soup.select("._d7c"):

				time.sleep(1)

				title = news.select("._PMs")[0].text # new title
				href = news.find("a")["href"]        # new hyper-link 
				print(title + " " + href)
				# 判斷現在的新聞,是否為新聞清單裡面,可以進行處理的
				now_href = [key for key in keys if key in href]
				if(now_href ==[]): # 如果不在清單裡，就跳到下一則新聞處理
					continue

				# 這篇新聞屬於哪個媒體
				now_press = taiwan_press[now_href[0]] 
				if now_press == "businessweekly": #單頁閱讀
					href = href + "&p=0"
                    
				# 讀取新聞的超連結
				news_res = requests.get(href, headers=headers)
				news_res.encoding = 'utf-8'
				news_soup = BeautifulSoup(news_res.text, "html.parser")

				# 用新聞標題當儲存文件的名稱
				file_name = title + ".txt"


				try:

					# 蘋果
					if (now_press == "apple"):
						content = news_soup.select(".clearmen")[0].text
						content = clean(now_press, content)

					# 自由
					elif (now_press == "ltn"):
						content = news_soup.select("#newstext")[0].text
						content = clean(now_press, content)

					# 中時
					elif (now_press == "chinatimes"):
						content = news_soup.select("article")[0].text
						content = clean(now_press, content)

					# 聯合新聞網
					elif (now_press == "udn.news"):
						content = news_soup.select("#story_body_content")[0].text
						content = clean(now_press, content)

					# 中央通訊社
					elif (now_press == "cna"):
						content = news_soup.select("section")[0].text
						content = clean(now_press, content)

					# 關鍵評論網
					elif (now_press == "thenewslens"):
						content = news_soup.select(".article-content")[0].text
						content = clean(now_press, content)

					# 風傳媒
					elif (now_press == "storm"):
						content = news_soup.select("article")[0].text
						content = clean(now_press, content)
                    
					# 商業週刊
					elif (now_press == "businessweekly"):
						content = news_soup.select(".be-changed")[0].text
						content = clean(now_press, content)

					# 公民行動
					elif (now_press == "civil"):
						content = news_soup.select(".clearfix")[0].text
						content = clean(now_press, content)
                        
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
			print('...Parsing...')

	# 新聞大表
	output_title.close()
	output_news.close()
	output_href.close()
	return( (news_output_path, title_output_path, href_output_path))
           


#==============================================================================================#
#================================= news_clean =================================================#
#==============================================================================================#
           
def clean(press, content):
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
		clean_content = clean_content.replace("\n", "")
		clean_content = clean_content.replace("\r", "")
		clean_content = clean_content.replace("\t", "")
		clean_content = clean_content.replace(" ", "")

       
	elif press == 'ltn':
		split_contents = clean_content.splitlines()
		clean_content = max(split_contents, key=len)
		clean_content = re.sub(r"\（.*?\）", '', clean_content) 
		clean_content = re.sub(r"\(.*?\)", '', clean_content) 
		clean_content = re.sub(r"\〔.*?\〕", '', clean_content)  
		clean_content = re.sub(r"\【.*?\】", '', clean_content)    
		clean_content = clean_content.replace("\n", "")
		clean_content = clean_content.replace("\r", "")
		clean_content = clean_content.replace("\t", "")
		clean_content = clean_content.replace(" ", "")

	elif press == 'chinatimes':
		split_contents = clean_content.splitlines()
		clean_content = max(split_contents, key=len)
		clean_content = re.sub(r"\（.*?\）", '', clean_content) 
		clean_content = re.sub(r"\(.*?\)", '', clean_content) 
		clean_content = re.sub(r"\〔.*?\〕", '', clean_content)  
		clean_content = re.sub(r"\【.*?\】", '', clean_content) 
		clean_content = clean_content.replace("\n", "")
		clean_content = clean_content.replace("\r", "")
		clean_content = clean_content.replace("\t", "")
		clean_content = clean_content.replace(" ", "")
  
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
		clean_content = clean_content.replace("\n", "")
		clean_content = clean_content.replace("\r", "")
		clean_content = clean_content.replace("\t", "")
		clean_content = clean_content.replace(" ", "")
    
	elif press == 'cna':
		split_contents = clean_content.splitlines()
		clean_content = max(split_contents, key=len)
		clean_content = re.sub(r"\（.*?\）", '', clean_content) 
		clean_content = re.sub(r"\(.*?\)", '', clean_content) 
		clean_content = re.sub(r"\〔.*?\〕", '', clean_content)  
		clean_content = re.sub(r"\【.*?\】", '', clean_content) 
		clean_content = re.sub(r"1060.*", '', clean_content) 
		clean_content = clean_content.replace("\n", "")
		clean_content = clean_content.replace("\r", "")
		clean_content = clean_content.replace("\t", "")
		clean_content = clean_content.replace(" ", "")
        
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
		clean_content = clean_content.replace("\r", "")
		clean_content = clean_content.replace("\t", "")
		clean_content = clean_content.replace(" ", "")
        
	elif press == 'storm': 
		clean_content = re.sub(r"\（.*?\）", '', clean_content) 
		clean_content = re.sub(r"\(.*?\)", '', clean_content) 
		clean_content = re.sub(r"\〔.*?\〕", '', clean_content)  
		clean_content = re.sub(r"\【.*?\】", '', clean_content) 
		clean_content = re.sub(r"[A-Za-z0-9]*", '', clean_content)
		clean_content = re.sub(r"[\.\{\;\)\}\#\/\—\'\,\@\-\&\:\[\]]*", '', clean_content)
		clean_content = clean_content.replace("年月日", "")
		clean_content = clean_content.replace("\’", "")
		clean_content = clean_content.replace("\n", "")
		clean_content = clean_content.replace("\r", "")
		clean_content = clean_content.replace("\t", "")
		clean_content = clean_content.replace(" ", "")
        
	elif press == "businessweekly": 
		clean_content = clean_content.replace("\n", "")
		clean_content = clean_content.replace("\r", "")
		clean_content = clean_content.replace("\t", "")
		clean_content = clean_content.replace(" ", "")
		clean_content = re.sub(r"資料整理：.*", '', clean_content)
        
	return(clean_content)

	return(content)




if __name__ == '__main__':
	print('this is main function')
