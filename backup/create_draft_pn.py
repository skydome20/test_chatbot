# -*- coding: utf-8 -*-

# create 'draft_proper_noun_txt' from getting titles of wiki articles
# 簡體字轉繁體字 （指令：opencc -i draft_proper_txt -o zh_draft_proper_txt ）
# The next step is to transform 'draft_proper_noun_txt' to 'proper_noun_txt'

import logging
import sys

from gensim.corpora.wikicorpus import extract_pages


def main():
	directroy = "/home/skydome20/Desktop/dbot/dbot.py3/wiki_article/"
	wiki_zip_name = directroy + "zhwiki-20161020-pages-articles.xml"


	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

	# get title, pagid from wiki_xml
	wiki_article = extract_pages(f = wiki_zip_name)

	texts_num = 0


	with open("proper_noun.txt",'w',encoding='utf-8') as output:

		for title, content, pageid in wiki_article:
			output.write(title + '\n')
			texts_num += 1
			if texts_num % 10000 == 0:
				logging.info("已處理 %d 篇文章" % texts_num)
	


if __name__ == "__main__":
	main()





