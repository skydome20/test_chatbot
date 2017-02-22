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
question = "客運致死"
#question = "台幣外匯"
#question = "論文造假"
# No filter #

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
keywords = news_module.news_associated_keywords(tabo_keywords, news_bigTable_path[1])
print(keywords)
news_bigTable_path = news_module.news_parse(keywords)
time.sleep(5)
#print('tabo', end="")
tabo_keywords.extend(news_module.keywords_tabo(keywords))
#print(tabo_keywords)

time.sleep(5)
print('3rd keywords:', end="")
keywords = news_module.news_associated_keywords(tabo_keywords, news_bigTable_path[1])
print(keywords)
news_bigTable_path = news_module.news_parse(keywords)
time.sleep(5)
#print('tabo', end="")
tabo_keywords.extend(news_module.keywords_tabo(keywords))
#print(tabo_keywords)

time.sleep(5)
print('4nd keywords:', end="")
keywords = news_module.news_associated_keywords(tabo_keywords, news_bigTable_path[1])
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
news_module.news_cut(news_bigTable_path[1])
time.sleep(5)
news_module.news_similar_filter(news_bigTable_path[1])
time.sleep(5)
keywords = news_module.news_associated_keywords(tabo_keywords, news_bigTable_path[1])
print(keywords)
news_bigTable_path = news_module.news_parse(keywords)
time.sleep(5)
#print('tabo', end="")
tabo_keywords.extend(news_module.keywords_tabo(keywords))
#print(tabo_keywords)

time.sleep(5)
print('3rd keywords:', end="")
news_module.news_cut(news_bigTable_path[1])
time.sleep(5)
news_module.news_similar_filter(news_bigTable_path[1])
time.sleep(5)
keywords = news_module.news_associated_keywords(tabo_keywords, news_bigTable_path[1])
print(keywords)
news_bigTable_path = news_module.news_parse(keywords)
time.sleep(5)
#print('tabo', end="")
tabo_keywords.extend(news_module.keywords_tabo(keywords))
#print(tabo_keywords)



time.sleep(5)
print('4nd keywords:', end="")
news_module.news_cut(news_bigTable_path[1])
time.sleep(5)
news_module.news_similar_filter(news_bigTable_path[1])
time.sleep(5)
keywords = news_module.news_associated_keywords(tabo_keywords, news_bigTable_path[1])
print(keywords)
#print('tabo', end="")
tabo_keywords.extend(news_module.keywords_tabo(keywords))
#print(tabo_keywords)
"""






