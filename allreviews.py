import csv
import os
import glob

privacy_keywords = ["privacy", "permission", "surveillance",
                    "advertisement","ads","confidential",
                    "monitor","intrusion","spy","confidential",
                   "private"]

security_keywords = ["security","protection","safety","safe",
                     "threat","targeted","secure","virus", "spyware", 
                     "malware","firewall","breach","exploit","bot"]
                     
creepy_keywords = ["creepy", "scary", "unusual","invasive",
                   "uncomfortable","violate","aware","unaware",
                  "spooky", "creep", "spy"]

data_keywords = ["data", "collection", "tos", "third-party",
                 "terms", "delete","save","policy","agree",
                 "agreement","consent","storage","information"]

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

gift_arr = ["gift", "present"]
people_arr = ["wife", "husband", "partner", "kid", "children", "child", "baby", 
				"toddler", "babies", "in-law", "mother", "father", "inlaw", "cousin",
				"brother", "sister", "grandparent", "grandma", "grandpa", "friend"]

PS_keywords = "privacy security individual fear leak protection breach violence " 
PS_keywords += "permission physical loss threat storage terrorism data cyber surveillance "
PS_keywords += "hack spy government monitor police violation crime violate abuse legal ethic " 
PS_keywords += "law freedom secret insurance confidential harm private damage nsa vulnerability "
PS_keywords += "fbi unauthorized creepy snowden cybersecurity track firewall "
PS_keywords += "privacy policy virus license agreement malware spyware antivirus"

PS_arr = PS_keywords.split(" ")
PS_arr += ["tos", "third-party", "secure"]
PS_arr += ["targeted", "advertisement", "ads", "scary", "unusual"]
PS_arr += ["uncomfortable", "safe", "safety", "invasive", "intrusion", "aware", "unaware", "right"]

PS_arr_multiplewords = ["third party", "terms of service", "privacy concern", "informed consent", "data collect", 
						"not aware"]

with open('all_reviews.csv', mode = 'w') as all_reviews_file:
	all_reviews_writer = csv.writer(all_reviews_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	all_reviews_writer.writerow(["source", "product", "version", "date", "verified", "rating", "content", "title","PS","privacy","security","creepy","data","camera","doorbell","voice","videocall","other","gift","people"])
	
	files = glob.glob(os.getcwd()+'/iga538/*.csv')
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

				PS_flag = 0

				if(any(x in content_arr for x in PS_arr) or any(x in title_arr for x in PS_arr) or 
							any(x in content for x in PS_arr_multiplewords) or any(x in title for x in PS_arr_multiplewords)):
					PS_flag = 1

				p,s,c,d,gift,people = 0,0,0,0,0,0
				if(any(x in content_arr for x in privacy_keywords) or any(x in title_arr for x in privacy_keywords)):
					p = 1
				if(any(x in content_arr for x in security_keywords) or any(x in title_arr for x in security_keywords)):
					s = 1
				if(any(x in content_arr for x in creepy_keywords) or any(x in title_arr for x in creepy_keywords)):
					c = 1
				if(any(x in content_arr for x in data_keywords) or any(x in title_arr for x in data_keywords)):
					d = 1
				if(any(x in content_arr for x in gift_arr) or any(x in title_arr for x in gift_arr)):
					gift = 1
				if(any(x in content_arr for x in people_arr) or any(x in title_arr for x in people_arr)):
					people = 1


				cam, doorbell, voice, video, other = 0, 0, 0, 0, 0

				date = row["date"]
				name = filename.split("-")[-1].split("_")
				if(len(name) == 2):
					product = name[0].strip()
					version = name[1].split(".")[0]
				else:
					product = name[0].split(".")[0].strip()
					version = ""

				if(product in camera_products):
					cam = 1
				elif(product in doorbell_products):
					doorbell = 1
				elif(product in voice_assistant_products):
					voice = 1
				elif(product in videocall_products):
					video = 1
				else:
					#print(name, product)
					other = 1

				verified = int(row["verified"])
				rating = float(row["rating"])
				all_reviews_writer.writerow([source, product, version, date, verified, rating, content, title, PS_flag, p, s, c, d, cam, doorbell, voice, video, other, gift, people])

