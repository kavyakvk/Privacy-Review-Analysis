# -*- coding: utf-8 -*- 
import scrapy 
import os 
import selectorlib 
from dateutil import parser as dateparser

class AmzSpider(scrapy.Spider): 
	name = 'amz' 
	allowed_domains = ['amazon.com/']
	start_urls = ['https://www.amazon.com/Echo-Studio/product-reviews/B07G9Y3ZMC/ref=cm_cr_arp_d_paging_btm_next_'+str(i)+'?ie=UTF8&reviewerType=all_reviews&pageNumber=' + str(i) for i in range(1,1200)] 
	#self._title_path = settings.get('TITLE_PATH', '')

	# Create Extractor for product page 
	product_page_extractor = selectorlib.Extractor.from_yaml_file(os.path.join(os.path.dirname(__file__),'../yaml/amazon_selectors.yml')) 
	
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
						row["location"] = r['date'].split("on ")[0]
						date_posted = r['date'].split('on ')[-1]
						row['date'] = dateparser.parse(date_posted).strftime('%d %b %Y')
						if("people found this helpful") in r:
							row['helpful'] = r['helpful'].split(" ")[0]
						row["author"] = r["author"]
						row["content"] = r["content"]
						row["title"] = r["title"]

						yield row
					else:
						print("duplicate author", len(self.author_data))
		# sleep(5)


