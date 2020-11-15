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

name = "scraped_data-BB-RingVideoDoorbellPro.csv"

class BBSpider(scrapy.Spider): 
	name = 'bb' 
	allowed_domains = ['bestbuy.com/']
	start_urls = ['https://www.bestbuy.com/site/reviews/ring-video-doorbell-pro-satin-nickel/5095900?variant=A&page='+str(i) for i in range(1,2000)] 
	# Create Extractor for product page 
	product_page_extractor = selectorlib.Extractor.from_yaml_file(os.path.join(os.path.dirname(__file__),'../yaml/best_buy_selectors.yml')) 
	
	author_data = set()

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
"""
process = CrawlerProcess()
process.crawl(BBSpider)
process.start(top_after_crawl=False)#s
process.stop()
"""
process = CrawlerProcess(settings={
    "FEEDS": {
        name: {"format": "csv"},
    },
})

process.crawl(BBSpider)
process.start()
"""
runner = CrawlerRunner()
d = runner.crawl(BBSpider)
d.addBoth(lambda _: reactor.stop())
#reactor.run() # the script will block here until the crawling is finished
"""


