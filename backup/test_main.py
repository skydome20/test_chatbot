import question_module
import news_test
import time


#news_bigTable_path = news_module.parse_news(first_keywords)
#news_bigTable_path[0] = title
#news_bigTable_path[1] = all
#news_bigTable_path[2] = href
#question = "川普當總統"
#question = "蔡英文最近的動向"
#question = "台灣教育和老師"
question = "一例一休的影響"
#question = "美國總統簽署行政命令"
#question = "論文造假"
#first_keywords = question_module.handler(question)
#news_bigTable_path = news_test.news_parse(first_keywords)
#news_module.news_cut(news_bigTable_path[1])

path = '/home/skydome20/Desktop/dbot/dbot.py3/news_folder/all/川普_簽署_行政命令.txt'

cut_news_path = news_test.news_cut(path)
time.sleep(5)
keep_ind = news_test.news_similar_filter(cut_news_path)
print(keep_ind)
news_test.news_summary('/home/skydome20/Desktop/dbot/dbot.py3/news_folder/title/川普_簽署_行政命令title.txt',
                       '/home/skydome20/Desktop/dbot/dbot.py3/news_folder/all/川普_簽署_行政命令.txt',
                       '/home/skydome20/Desktop/dbot/dbot.py3/news_folder/href/川普_簽署_行政命令_href.txt',
                       keep_ind)













