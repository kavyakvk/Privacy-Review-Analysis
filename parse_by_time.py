import csv
import os
import glob
from datetime import datetime

def parse_time(d):
	if("-" in d):
		dt = datetime.strptime(d, '%d-%b-%y')
	else:
		dt = datetime.strptime(d, '%d %b %Y')
	year = dt.year
	month = dt.month

	return month, year

with open("aggregated_reviews.csv", mode='r') as read_file:
	reader = csv.DictReader(read_file)
	with open("time_aggregated_reviews.csv", mode="w") as write_file:
		writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		last_index = (2020-2015)
		index_labels = [i for i in range(last_index+1)]
		#index_labels.append(str(i%12 + 1)+"-\'"+str(i//12 + 2010))
		writer.writerow(["product", "keyword"]+index_labels)

		trends = {}
			
		for row in reader:
			#["source", "product", "version", "date", "verified", "rating", 
			#"content", "title", "gift", "keywords", "people_keywords"]
			month, year = parse_time(row["date"])
			#index: years since january 2010 (0)
			index = (year-2015)

			product = row["product"]

			if(product not in trends.keys()):
				trends[product] = {}

			for keyword in row["keywords"].split(","):
				if(keyword != "" and keyword != " "):
					keyword = keyword.strip()
					if(keyword not in trends[product].keys()):
						trends[product][keyword] = [0 for i in range(last_index+1)]
					trends[product][keyword][index] += 1

		total_reviews = {}
		cwd = os.getcwd()
		files = glob.glob(cwd+'/iga538/*.csv')
		for filename in files:
			file = open(filename)
			temp_reader = csv.DictReader(file)

			name = filename.split("-")[-1].split("_")
			if(len(name) == 2):
				product = name[0]
				version = name[1].split(".")[0]
			else:
				product = name[0].split(".")[0]
				version = ""

			if("BB" in filename):
				source = "BB"
			else:
				source = "AMZ"

			if(product not in total_reviews.keys()):
				total_reviews[product] = [0 for i in range(last_index+1)]

			print(filename)
			for row in temp_reader:
				#print(row["date"])
				month, year = parse_time(row["date"])
				if(year < 2015):
					print(year)
				else:
					total_reviews[product][year-2015] +=1

		for p in trends.keys():
			for k in trends[p].keys():
				norm_row = [i/sum(total_reviews[p]) for i in trends[p][k]]
				if(len([*filter(lambda x: x >= 0.0001, norm_row)]) > 0):
					writer.writerow([p,k]+norm_row)
