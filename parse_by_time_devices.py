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

privacy_keywords = ["privacy", "permission", "surveillance",
                    "advertisement","ads","confidential",
                    "monitor","intrusion","spy","confidential",
                   "private"]

security_keywords = ["security","protection","safety","safe",
                     "threat","targeted","secure","virus", "spyware", 
                     "malware","firewall","breach","exploit","bot"]

creepy_keywords = ["creepy", "scary", "unusual","invasive",
                   "uncomfortable","violate","aware","unaware",
                  "spooky", "creep"]

data_keywords = ["data", "collection", "tos", "third-party",
                 "terms", "delete","save","policy","agree",
                 "agreement","consent","storage","information"]

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

	with open("time_aggregated_reviews_devices-normalized.csv", mode="w") as write_file:
		writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		df = pd.read_csv("all_reviews.csv",dtype={'version': 'string'})
		df.fillna("N/A", inplace=True)

		last_index = (2020-2015)*4+4
		index_labels = [i for i in range(last_index+1)]
		#index_labels.append(str(i%12 + 1)+"-\'"+str(i//12 + 2010))
		writer.writerow(["device-group","product", "topic", "subject","time","frac-reviews","avg-rating"])#+index_labels

		trends = {}
		trends["All"] = {}

		for subject_topic in LDA_reviews.keys():
			subject = subject_topic.split("-")[0]
			topic = subject_topic.split("-")[1].split(":")[0]

			for idx in LDA_reviews[subject_topic]:
				row = df.iloc[idx]
				product = row["product"]

				if(product not in trends.keys()):
					trends[product] = {}
				if(subject not in trends[product].keys()):
					trends[product][subject] = {}
				if(topic not in trends[product][subject].keys()):
					trends[product][subject][topic] = [[0,0] for i in range(last_index+1)]

				if(subject not in trends["All"].keys()):
					trends["All"][subject] = {}
				if(topic not in trends["All"][subject].keys()):
					trends["All"][subject][topic] = [[0,0] for i in range(last_index+1)]

				month, year = parse_time(row["date"])

				quarter = (year-2015)*4+(month//4)
				trends[product][subject][topic][quarter][0] += 1
				trends["All"][subject][topic][quarter][0] += 1
				trends[product][subject][topic][quarter][1] += row["rating"]
				trends["All"][subject][topic][quarter][1] += row["rating"]

		total_reviews = {}
		total_reviews["All"] = [0 for i in range(last_index+1)]
		total_ratings = {}
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
		#print(ordering)
		ordering.remove("All")
		#print(ordering)
		ordering.extend(["All"])
		#print(ordering)

		for p in ordering:
			if(True):
				norm_row[p] = {}
				norm_rating_row[p] = {}
				for s in trends[p].keys():
					norm_row[p][s] = {}
					norm_rating_row[p][s] = {}
					for t in trends[p][s].keys():
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

						norm_row[p][s][t] = [i[0]/sum(total_reviews[p]) for i in trends[p][s][t]]
						if(p != "All"):
							norm_rating_row[p][s][t] = [(i[1]/i[0]) if i[0] > 0 else 1 for i in trends[p][s][t]]
						else:
							norm_rating_row[p][s][t] = [0 for i in trends[p][s][t]]
							
							for q in range(len(trends[p][s][t])):
								counter = 0
								for d in ordering[:-1]:
									if (d == "All"):
										print(d, "All")
									elif(d in trends.keys() and s in trends[d].keys() and t in trends[d][s].keys()):
										if(norm_rating_row[d][s][t][q] > 1):
											counter += 1
											norm_rating_row[p][s][t][q] += norm_rating_row[d][s][t][q]

								if(counter == 0):
									norm_rating_row[p][s][t][q] = 1
								else:
									norm_rating_row[p][s][t][q] = norm_rating_row[p][s][t][q]/counter

						for q in range(len(norm_row[p][s][t])):
							if(len([*filter(lambda x: x >= 0.0001, norm_row[p][s][t])]) > 0):
								writer.writerow([device, p, s, t, q, norm_row[p][s][t][q], norm_rating_row[p][s][t][q]])





