import csv
import os
import glob
from datetime import datetime
import pickle
import pandas as pd

camera_products = ["NestOutdoorCam","NestMini","NestIndoorCam",
                   "WyzeCamPan","NanitPlus","ArloPro",
                   "RingStickUpCam","RingSpotlightCam","RingIndoorCam","RingFloodlightCam"]
doorbell_products = ["RingVideoDoorbell","NestVideoDoorbell"]
voice_assistant_products = ["GoogleHomeMini","NestMini",
                            "Homepod",
                            "EchoFlex","EchoDot"]
videocall_products = ["EchoShow","EchoStudio",
                     "NestHubMax","FacebookPortal"]
other_products = ["NestWifi","NestThermostat"]

topics_list = ["PS", "privacy","security","creepy","data","all reviews"]

def parse_time(d):
	if("-" in d):
		dt = datetime.strptime(d, '%d-%b-%y')
	else:
		dt = datetime.strptime(d, '%d %b %Y')
	year = dt.year
	month = dt.month

	return month, year

if(True):
	LDA_reviews = pickle.load(open('LDA_indexes', 'rb'))
									#-normalized
	with open("time_aggregated_reviews_keywords-normalized.csv", mode="w") as write_file:
		writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		df = pd.read_csv("all_reviews.csv",dtype={'version': 'string'})
		df.fillna("N/A", inplace=True)

		last_index = (2020-2015)*4+4
		index_labels = [i for i in range(last_index+1)]
		#index_labels.append(str(i%12 + 1)+"-\'"+str(i//12 + 2010))
		writer.writerow(["device-group","product", "topic", "time","frac-reviews","avg-rating"])#+index_labels

		trends = {}
		trends["All"] = {}

		for idx in df.index:
			row = df.iloc[idx]
			product = row["product"]

			for topic in topics_list:
				if(topic == "all reviews" or row[topic] == 1):
					if(product not in trends.keys()):
						trends[product] = {}
					if(topic not in trends[product].keys()):
						trends[product][topic] = [[0,0] for i in range(last_index+1)]

					if(topic not in trends["All"].keys()):
						trends["All"][topic] = [[0,0] for i in range(last_index+1)]

					month, year = parse_time(row["date"])

					quarter = (year-2015)*4+(month//4)

					if(quarter < 0 or quarter > 24):
						print(quarter, product, topic, len(trends[product][topic]))
					else:
						trends[product][topic][quarter][0] += 1
						trends["All"][topic][quarter][0] += 1
						trends[product][topic][quarter][1] += row["rating"]
						trends["All"][topic][quarter][1] += row["rating"]


		total_reviews = {}
		total_reviews["All"] = [0 for i in range(last_index+1)]
		for ind in df.index: 
			p = df.iloc[ind]["product"]
			if(p not in total_reviews.keys()):
				total_reviews[p] = [0 for i in range(last_index+1)]
			
			month, year = parse_time(row["date"])
			quarter = (year-2015)*4+(month//4)
			total_reviews[p][quarter] += 1
			total_reviews["All"][quarter] += 1

		norm_row = {}
		norm_rating_row = {}
		ordering = list(trends.keys())
		ordering.remove("All")
		ordering.extend(["All"])
		for p in ordering:
			norm_row[p] = {}
			norm_rating_row[p] = {}
			for t in trends[p].keys():
				device = ""
				if(p in camera_products):
					device = "Cameras"
				elif(p in doorbell_products):
					device = "Doorbell"
				elif(p in voice_assistant_products):
					device = "Voice Assistants"
				elif(p in videocall_products):
					device = "Video Platforms"
				elif(p in other_products):
					device = "Other"
				else:
					device = "All"

				norm_row[p][t] = [i[0]/sum(total_reviews[p]) for i in trends[p][t]]
				if(p != "All"):
					norm_rating_row[p][t] = [(i[1]/i[0]) if i[0] > 0 else 1 for i in trends[p][t]]
				else:
					norm_rating_row[p][t] = [0 for i in trends[p][t]]
					
					for q in range(len(trends[p][t])):
						counter = 0
						for d in ordering[:-1]:
							if (d == "All"):
								print(d, "All")
							elif(d in trends.keys() and t in trends[d].keys()):
								if(norm_rating_row[d][t][q] > 1):
									counter += 1
									norm_rating_row[p][t][q] += norm_rating_row[d][t][q]
						
						if(counter == 0):
							norm_rating_row[p][t][q] = 1
						else:
							norm_rating_row[p][t][q] = norm_rating_row[p][t][q]/counter

				for q in range(len(norm_row[p][t])):
					if(len([*filter(lambda x: x >= 0.0001, norm_row[p][t])]) > 0):
						writer.writerow([device, p, t, q, norm_row[p][t][q],norm_rating_row[p][t][q]])
