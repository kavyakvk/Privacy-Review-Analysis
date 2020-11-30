# Privacy-Review-Analysis
My final project for IGA 538, Technology, Privacy, and the Trans-National Nature of the Internet. 

## Overview of Project
Smart home assistants like Amazon Alexa and Google Home have become ubiquitous in households across the world. This rise is coupled with a significant adoption of IoT (internet of things)-enabled devices, from smart thermostats to smart home security cameras. However, there has been a significant shift in the reasonable expectation of privacy in the home with this large influx of sensor-enabled devices into traditionally “private” spaces. 

## Overview of Technology
### Using Scrapy and SelectorLib to Scrape Websites
The following websites (which contain customer reviews of different home IoT products) were scraped for this project:
	* Amazon.com (change version in run_spiders to "AMZ")
	* BestBuy.com (change version in run_spiders to "BB")

```
python3 run_spiders.py
```

### Getting Aggregate Statistics
Getting a csv with P&S reviews and a csv with metadata:
```
	python3 reviews_with_PS_words.py
```
Getting a csv for Topic Modeling:
```
	python3 allreviews.py
```

### Topic Modeling
