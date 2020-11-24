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
"""
process = CrawlerProcess()
process.crawl(BBSpider)
process.start(top_after_crawl=False)#s
process.stop()
"""

names = ["BB-NanitPlus","BB-ArloPro","BB-NestIndoorCam","BB-NestOutdoorCam",
		"BB-RingStickUpCam","BB-RingSpotlightCam",
		"BB-RingFloodlightCam","BB-RingVideoDoorbell3","BB-RingVideoDoorbell3Plus",
		"BB-EchoFlex","BB-NestWifi_3Pack","BB-NestWifi_2Pack", "BB-NestWifi",
		"BB-NestThermostat"]
urls = ['https://www.bestbuy.com/site/reviews/nanit-plus-smart-baby-monitor-wall-mount-white/6304010?variant=A',
		'https://www.bestbuy.com/site/reviews/arlo-pro-3-4-camera-indoor-outdoor-wire-free-2k-hdr-security-camera-system-black/6364584?variant=A',
		'https://www.bestbuy.com/site/reviews/google-nest-cam-indoor-security-camera-black/6473147?variant=A',
		'https://www.bestbuy.com/site/reviews/google-nest-cam-outdoor-security-camera-white/5451208?variant=A',
		'https://www.bestbuy.com/site/reviews/ring-stick-up-indoor-outdoor-wire-free-1080p-security-camera-black/6403964?variant=A',
		'https://www.bestbuy.com/site/reviews/ring-spotlight-cam-wire-free-white/5936903?variant=A',
		'https://www.bestbuy.com/site/reviews/ring-floodlight-cam-white/5839407?variant=A',
		"https://www.bestbuy.com/site/reviews/ring-video-doorbell-3-satin-nickel/6402552?variant=A",
		"https://www.bestbuy.com/site/reviews/ring-video-doorbell-3-plus-satin-nickel/6402551?variant=A",
		"https://www.bestbuy.com/site/reviews/amazon-echo-flex-smart-speaker-with-alexa-white/6380475?variant=A",
		"https://www.bestbuy.com/site/reviews/google-nest-wifi-ac2200-mesh-system-router-and-2-add-on-points-3-pack-snow/6382518?variant=A",
		"https://www.bestbuy.com/site/reviews/google-nest-wifi-ac2200-mesh-system-router-and-point-2-pack-snow/6382512?variant=A",
		"https://www.bestbuy.com/site/reviews/google-nest-wifi-ac2200-router-snow/6382499?variant=A",
		"https://www.bestbuy.com/site/reviews/google-nest-learning-smart-thermostat-3rd-generation-white/5852329?variant=A"]

i=1

n = names[i]
url = urls[i]

name = "scraped_data-"+n+".csv"
#start_urls = [url+'&page='+str(i) for i in range(1,100)] 
start_urls = ["https://www.bestbuy.com/site/reviews/arlo-pro-3-4-camera-indoor-outdoor-wire-free-2k-hdr-security-camera-system-black/6364584?page="+str(i) for i in range(1,100)]
try:
	process = CrawlerProcess(settings={
		"FEEDS": {
			name: {"format": "csv"},
		},
	})
	process.crawl(BBSpider, start_urls=start_urls)
	process.start()
except:
	print("caught the error!")
	process.stop()

process = None

print("IM DONE! :)")
"""
runner = CrawlerRunner()
d = runner.crawl(BBSpider)
d.addBoth(lambda _: reactor.stop())
#reactor.run() # the script will block here until the crawling is finished
"""


