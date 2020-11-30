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
from iga538.iga538.spiders.amz import AmzSpider
from iga538.iga538.spiders.bb import BBSpider

version = "BB"
i=0

if(version == "BB"):
	names = ["BB-NanitPlus","BB-ArloPro","BB-NestIndoorCam","BB-NestOutdoorCam",
			"BB-RingStickUpCam","BB-RingSpotlightCam",
			"BB-RingFloodlightCam","BB-RingVideoDoorbell3","BB-RingVideoDoorbell3Plus",
			"BB-EchoFlex","BB-NestWifi_3Pack","BB-NestWifi_2Pack", "BB-NestWifi",
			"BB-NestThermostat","BB-EchoDot_3Gen"]
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
			"https://www.bestbuy.com/site/reviews/google-nest-learning-smart-thermostat-3rd-generation-white/5852329?variant=A",
			"https://www.bestbuy.com/site/reviews/amazon-echo-dot-3rd-gen-smart-speaker-with-alexa-sandstone/6287976?variant=A"]

	n = names[i]
	url = urls[i]

	name = "iga538/scraped_data-"+n+".csv" 
	start_urls = [url+"&page="+str(i) for i in range(1,100)]
else:
	names = ["EchoFlex","EchoDot"]
	urls = ["https://www.amazon.com/Echo-Flex/product-reviews/B07MLY3JKV/",
			"https://www.amazon.com/Echo-Dot/product-reviews/B07FZ8S74R/"]

	n = names[i]
	url = urls[i]

	name = "iga538/scraped_data-"+n+".csv"
	start_urls = [url+str(i)+'ref=cm_cr_arp_d_paging_btm_next_'+str(i)+'?ie=UTF8&reviewerType=all_reviews&pageNumber=' + str(i) for i in range(1,1200)]

try:
	process = CrawlerProcess(settings={
		"FEEDS": {
			name: {"format": "csv"},
		},
	})
	if(version == "BB"):
		process.crawl(BBSpider, start_urls=start_urls)
	else:
		process.crawl(AmzSpider, start_urls=start_urls)
	process.start()
except:
	print("caught the error!")
	process.stop()

process = None

print("IM DONE! :)")


