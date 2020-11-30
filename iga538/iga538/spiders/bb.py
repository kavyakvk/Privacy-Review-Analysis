# -*- coding: utf-8 -*- 
import scrapy 
import os 
import selectorlib 
from dateutil import parser as dateparser
from dateutil import relativedelta
import datetime
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor
from scrapy.exporters import CsvItemExporter
from scrapy.utils.project import get_project_settings

class BBSpider(scrapy.Spider): 

	def __init__(self, start_urls, **kwargs):
		self.name = 'bb' 
		self.start_urls = start_urls
		self.allowed_domains = ['bestbuy.com/']
		# Create Extractor for product page 
		self.product_page_extractor = selectorlib.Extractor.from_yaml_file(os.path.join(os.path.dirname(__file__),'../yaml/best_buy_selectors.yml')) 
		
		self.author_data = set()
		super().__init__(**kwargs)  # python3

	def parse(self, response): 
		# Extract data using Extractor 
		response_text = self.product_page_extractor.extract(response.text)
		#print(data)
		row = {}
		data_bulk = response_text["bulk_review_block"]
		#print(response_text["num_ratings"])
		if data_bulk:
			for data in data_bulk:
				#print("data reviews: " + str(data.keys()))
				for r in data['reviews']:
					size = len(self.author_data)
					self.author_data.add(r['author'])
					if(len(self.author_data) > size):
						#print("new author")
						row["product"] = response_text["product_title"]
						if 'Verified Purchase' in r['verified']:
							row['verified'] = 1
						else:
							row['verified'] = 0
						
						row['rating'] = r['rating'].split(' out of')[0]
						row['rating'] = row['rating'].split(' ')[1]

						review_time = datetime.date.today()
						time_num = int(r['date'].split(" ")[0])
						if("month" in r['date']):
							review_time -= relativedelta.relativedelta(months=time_num)
						elif("hour" in r['date']):
							review_time -= relativedelta.relativedelta(hours=time_num)
						elif("day" in r['date']):
							review_time -= relativedelta.relativedelta(days=time_num)
						else: #year
							review_time -= relativedelta.relativedelta(years=time_num)
						row['date'] = review_time.strftime('%d %b %Y')

						if("Helpful") in r:
							row['helpful'] = r['helpful'].split("Helpful (")[0]

						row["author"] = r["author"]
						row["content"] = r["content"]
						row["title"] = r["title"]

						yield row
					else:
						print("duplicate author", len(self.author_data))
		# sleep(5)
