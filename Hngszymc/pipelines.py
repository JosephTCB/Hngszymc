# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json,re
class HngszymcPipeline(object):
	def process_item(self, item, spider):
		return item

	def __init__(self):
		self.f = open("hngszymc.json", "w+",encoding='utf-8')

		  # 所有的item使用共同的管道
	def process_item(self, item, spider):
		content = json.dumps(dict(item), ensure_ascii = False) + ",\n"
		self.f.write(content)
		return item

	def close_spider(self, spider):
		self.f.close()
		f = open('hngszymc.json', 'r', encoding='utf-8')
		result = ""
		for line in open('hngszymc.json', encoding='utf-8'):
			line = f.readline()
			result = result + line
		f.close()
		result = result[:-2]
		result = "[" + result + "]"
		load_dict = json.loads(result)
		qalist = []
		for load in load_dict:
			if (not (load['q'].strip() == '' or load['a'].strip() == '')):
				if (not (load['a'].strip().startswith('【业务概述】'))):
					start = load['a'].find('【业务概述】')
					r = re.match(r'^[-0123456789—.]*', load['q']).group()
					q = load['q'].replace(r, '', 1).replace(' ', '').replace('*', '')
					qa = {'q': q, 'a': load['a'][start:]}
					qalist.append(qa)
		file = open('hngszymc.txt', 'w', encoding='utf-8')
		for q_a in qalist:
			content = json.dumps(q_a, ensure_ascii=False) + ',\n'
			file.write(content)
		file.close()
