import question_module
import news_module
import time

#news_bigTable_path = news_module.parse_news(first_keywords)
#news_bigTable_path[0] = title
#news_bigTable_path[1] = all
#news_bigTable_path[2] = href

#question = "蔡英文最近的動向"
#question = "台灣教育和老師"
#question = "川普簽署行政命令"
#question = "一例一休的影響"
#question = "升學制度與大學"
#question = "內閣改組的影響"
#question = "墨西哥長牆"
#question = "Uber的罰款議題"
#question = "中國與美國未來的關係"
#question = "大學評鑑"
#question = "客運致死"
#question = "台幣外匯"
#question = "台大論文造假"
#question = "女大生去麵包坊實習被索賠"
question = "最近石油的影響或走向"
# No filter #
"""
tabo_keywords = []
print("============= No filter ===============")
print('1st keywords:', end="") 
keywords = question_module.handler(question)
print(keywords)
news_bigTable_path = news_module.news_parse(keywords)
time.sleep(5)
#print('tabo', end="")
tabo_keywords.extend(news_module.keywords_tabo(keywords))
#print(tabo_keywords)

time.sleep(5)
print('2nd keywords:', end="")
cut_news_path = news_module.news_cut(news_bigTable_path[1])
keywords = news_module.news_associated_keywords(tabo_keywords, cut_news_path)
print(keywords)
news_bigTable_path = news_module.news_parse(keywords)
time.sleep(5)
#print('tabo', end="")
tabo_keywords.extend(news_module.keywords_tabo(keywords))
#print(tabo_keywords)

time.sleep(5)
print('3rd keywords:', end="")
cut_news_path = news_module.news_cut(news_bigTable_path[1])
keywords = news_module.news_associated_keywords(tabo_keywords, cut_news_path)
print(keywords)
news_bigTable_path = news_module.news_parse(keywords)
time.sleep(5)
#print('tabo', end="")
tabo_keywords.extend(news_module.keywords_tabo(keywords))
#print(tabo_keywords)

time.sleep(5)
print('4nd keywords:', end="")
cut_news_path = news_module.news_cut(news_bigTable_path[1])
keywords = news_module.news_associated_keywords(tabo_keywords, cut_news_path)
print(keywords)
#print('tabo', end="")
tabo_keywords.extend(news_module.keywords_tabo(keywords))
#print(tabo_keywords)




"""

# Similar filter #
tabo_keywords = []
print("============= Similar filter ===============")
print('1st keywords:', end="") 
keywords = question_module.handler(question)
print(keywords)
news_bigTable_path = news_module.news_parse(keywords)
time.sleep(5)
#print('tabo', end="")
tabo_keywords.extend(news_module.keywords_tabo(keywords))
#print(tabo_keywords)

time.sleep(5)
print('2nd keywords:', end="")
cut_news_path = news_module.news_cut(news_bigTable_path[1])
time.sleep(5)
filter_news_path = news_module.news_similar_filter(cut_news_path)
time.sleep(5)
keywords = news_module.news_associated_keywords(tabo_keywords, filter_news_path)
print(keywords)
news_bigTable_path = news_module.news_parse(keywords)
time.sleep(5)
#print('tabo', end="")
tabo_keywords.extend(news_module.keywords_tabo(keywords))
#print(tabo_keywords)

time.sleep(5)
print('3rd keywords:', end="")
cut_news_path = news_module.news_cut(news_bigTable_path[1])
time.sleep(5)
filter_news_path = news_module.news_similar_filter(cut_news_path)
time.sleep(5)
keywords = news_module.news_associated_keywords(tabo_keywords, filter_news_path)
print(keywords)
news_bigTable_path = news_module.news_parse(keywords)
time.sleep(5)
#print('tabo', end="")
tabo_keywords.extend(news_module.keywords_tabo(keywords))
#print(tabo_keywords)



time.sleep(5)
print('4nd keywords:', end="")
cut_news_path = news_module.news_cut(news_bigTable_path[1])
time.sleep(5)
filter_news_path = news_module.news_similar_filter(cut_news_path)
time.sleep(5)
keywords = news_module.news_associated_keywords(tabo_keywords, filter_news_path)
print(keywords)
#print('tabo', end="")
tabo_keywords.extend(news_module.keywords_tabo(keywords))
#print(tabo_keywords)







