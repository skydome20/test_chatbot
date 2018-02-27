# -*- coding: utf-8 -*-

# 簡體字轉繁體字後 （指令：opencc -i draft_proper_txt -o zh_draft_proper_txt ）
# Transform 'zh_draft_proper_noun_txt' to 'zh_proper_noun_txt'

import logging
import sys


def main():
	directroy = "/home/skydome20/Desktop/dbot/dbot.py3/jieba_dict/"
	input_name = directroy + "zh_draft_proper_noun.txt"
	output_name = directroy + "zh_proper_noun.txt"

	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

	title_num = 0
	
	fin = open(input_name, 'r', encoding='utf-8')
	fout = open(output_name, 'w', encoding='utf-8')


	# remove noise
	for line in fin.readlines():
		if "Wikipedia:" in line:
			continue
		if "Help:" in line: 
			continue
		if "Category:" in line: 
			continue
		if "Template:" in line: 
			continue
		if "File:" in line: 
			continue
		if ".jpg" in line: 
			continue

		if "(" in line:
			fout.write(line.split(" ")[0])
			title_num += 1
			continue
		if "·" in line:
			for name in line.split("·"):
				fout.write(name)
				
			title_num += 1
			continue

		fout.write(line)
		title_num += 1

		if title_num % 10000 == 0:
			logging.info("已處理 %d 則標題" % title_num)

		
	fin.close()
	fout.close()

	# remove duplicated lines
	lines = open(output_name, 'r', encoding='utf-8').readlines()
	lines_set = set(lines)

	fout  = open(output_name, 'w')
	for line in lines_set:
		output = line.rstrip() + " 3" + "\n"
		fout.write(output)
	fout.close()


if __name__ == "__main__":
	main()





