import csv
import os
import glob

PS_keywords = "privacy security individual fear leak protection breach violence " 
PS_keywords += "permission physical loss threat storage terrorism data cyber surveillance "
PS_keywords += "hack spy government monitor police violation crime violate abuse legal ethic " 
PS_keywords += "law freedom secret insurance confidential harm private damage nsa vulnerability "
PS_keywords += "fbi unauthorized creepy snowden cybersecurity track firewall "
PS_keywords += "privacy policy virus license agreement malware spyware antivirus"

PS_arr = PS_keywords.split(" ")
PS_arr += ["tos", "third-party", "secure"]
PS_arr += ["targeted", "advertisement", "ads", "scary", "unusual"]
PS_arr += ["uncomfortable", "safe", "safety", "invasive", "intrusion"]

PS_arr_multiplewords = ["third party", "terms of service", "privacy concern", "informed consent"]

gift_arr = ["gift", "present"]
people_arr = ["wife", "husband", "partner", "kids", "children", "child", "baby", 
				"todler", "babies", "in-law", "mother", "father", "inlaw", "cousin",
				"brother", "sister", "grandparent", "grandma", "grandpa"]

counter = 0

with open("metadata.csv", mode="w") as metadata_file:
	metadata_writer = csv.writer(metadata_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	metadata_writer.writerow(["product", "version", "source", "total reviews", "P&S reviews",
								"non-P&S 0 reviews","non-P&S 1 reviews","non-P&S 2 reviews","non-P&S 3 reviews","non-P&S 4 reviews","non-P&S 5 reviews",
								"P&S 0 reviews","P&S 1 reviews","P&S 2 reviews","P&S 3 reviews","P&S 4 reviews","P&S 5 reviews"])

	with open('aggregated_reviews.csv', mode='w') as write_file:
		writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(["source", "product", "version", "date", "verified", "rating", "content", "title", "gift", "keywords", "people_keywords"])
		cwd = os.getcwd()
		files = glob.glob(cwd+'/iga538/*.csv')
		
		for filename in files:
			print(filename)
			rating_arr = [[0,0,0,0,0,0], [0,0,0,0,0,0]] #non P&S review, P&S reviews
			file_counters = [0,0] #total num reviews, P&S reviews
			product_name = ""
			version_name = ""

			with open(filename, mode='r') as read_file:
				reader = csv.DictReader(read_file)
				source = ""
				for row in reader:
						if("BB" in filename):
							source = "BB"
						else:
							source = "AMZ"
						
						content = row["content"]
						title = row["title"]
						content_arr = content.lower().split(" ")
						title_arr = title.lower().split(" ")

						if(any(x in content_arr for x in PS_arr) or any(x in title_arr for x in PS_arr) or 
							any(x in content for x in PS_arr_multiplewords) or any(x in title for x in PS_arr_multiplewords)):
							keywords = ""

							for w in PS_arr:
								if(w in content_arr or w in title_arr):
									keywords = keywords + w + ", "

							if(any(x in content_arr for x in gift_arr) or any(x in title_arr for x in gift_arr)):
								gift = 1
							else:
								gift = 0

							people_keywords = ""
							if(any(x in content_arr for x in people_arr) or any(x in title_arr for x in people_arr)):
								for w in people_arr:
									if(w in content_arr or w in title_arr):
										people_keywords = people_keywords + w + ", "

							date = row["date"]
							name = filename.split("-")[-1].split("_")
							if(len(name) == 2):
								product = name[0]
								version = name[1].split(".")[0]
							else:
								product = name[0].split(".")[0]
								version = ""

							verified = int(row["verified"])
							rating = float(row["rating"])
							writer.writerow([source, product, version, date, verified, rating, content, title, gift, keywords, people_keywords])
							
							counter += 1
							file_counters[1] += 1
							rating_arr[1][round(rating)] += 1
							product_name = product
							version_name = version
							print(counter)
						else:
							if(row["rating"] != "rating"):
								rating = float(row["rating"])
								rating_arr[0][round(rating)] += 1
						file_counters[0] += 1
				
				metadata_writer.writerow([product_name, version_name, source]+file_counters+rating_arr[0]+rating_arr[1])
