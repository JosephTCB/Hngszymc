# coding: utf-8
from scrapy import Spider
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import etree
from Hngszymc.items import HngszymcItem

class HnQaSpider(Spider):
	name = 'qa'
	allowed_domains = ['dzhy.ha-n-tax.gov.cn']
	start_urls = ['http://dzhy.ha-n-tax.gov.cn/web/gccx/getDzhy_lcclass_all.do?RELEASE_DM=2']
	def parse(self, response):
		# chrome_options = webdriver.ChromeOptions()
		# chrome_options.add_argument('--headless')
		# chrome_options.add_argument('--disable-gpu')
		# driver = webdriver.Chrome(chrome_options=chrome_options)
		driver = webdriver.Chrome()
		driver.implicitly_wait(30)
		driver.get(self.start_urls[0])
		html = etree.HTML(driver.page_source)
		nagivationlist = html.xpath('//a[not(contains(text(),"."))][not(contains(text(),"办税指南"))][@id]')
		js = " window.open('http://dzhy.ha-n-tax.gov.cn/web/gccx/getDzhy_lcclass_all.do?RELEASE_DM=2')"
		driver.execute_script(js)
		handles = driver.window_handles
		time.sleep(1)
		driver.switch_to_window(handles[0])
		for nagivation in nagivationlist:
			driver.get('http://dzhy.ha-n-tax.gov.cn/web/gccx/'+nagivation.get('href'))
			time.sleep(2)
			nodelist = etree.HTML(driver.page_source).xpath('//td[2]/a')
			driver.switch_to_window(handles[1])
			time.sleep(1)
			for node in nodelist:
				try:
					driver.get('http://dzhy.ha-n-tax.gov.cn/web/gccx/' + node.get('href'))
					time.sleep(1)
					question = BeautifulSoup(driver.page_source, 'lxml').select('span#titleMsgDiv')[0].text
					driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
					ps = BeautifulSoup(driver.page_source, 'lxml').select('p')
					i = 0
					lc = 0
					for p in ps:
						if p.text.find('【业务流程】') != -1 or p.text.find('【办理流程】') != -1:
							lc = i
						i = i + 1
					answer = ''
					for i in range(lc):
						answer = answer + ps[i].text
					print(question)
					print(answer)
					item = HngszymcItem()
					item['q'] = question
					item['a'] = answer
					yield item
					time.sleep(2)
				except:
					time.sleep(3)
					break
			driver.switch_to_window(handles[0])
			time.sleep(1)
			while len(etree.HTML(driver.page_source).xpath(
							'//a[contains(text(),"下一页")][contains(@href,"onQueryByPage")]'))==1:
				driver.find_elements_by_xpath(
					'//a[contains(text(),"下一页")][contains(@href,"onQueryByPage")]')[0].click()
				time.sleep(2)
				nodelist = etree.HTML(driver.page_source).xpath('//td[2]/a')
				driver.switch_to_window(handles[1])
				time.sleep(2)
				for node in nodelist:
					try:
						driver.get('http://dzhy.ha-n-tax.gov.cn/web/gccx/' + node.get('href'))
						time.sleep(1)
						question = BeautifulSoup(driver.page_source, 'lxml').select('span#titleMsgDiv')[0].text
						driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
						ps = BeautifulSoup(driver.page_source, 'lxml').select('p')
						i = 0
						lc = 0
						for p in ps:
							if p.text.find('【业务流程】')!=-1 or p.text.find('【办理流程】')!=-1:
								lc = i
							i = i + 1
						answer=''
						for i in range(lc):
							answer = answer + ps[i].text
						print(question)
						print(answer)
						item = HngszymcItem()
						item['q'] = question
						item['a'] = answer
						yield item
						time.sleep(2)
					except:
						time.sleep(3)
						break
				driver.switch_to_window(handles[0])
				time.sleep(2)



