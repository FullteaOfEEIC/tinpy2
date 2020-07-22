infos = json.load(open("infos.json", "r"))

FB_email = infos["mail"]
FB_pass = infos["pass"]
latitude, longitude = infos["location"]

db_username = "root"
db_pass = "root"
db_host = "tinpy2_db"
