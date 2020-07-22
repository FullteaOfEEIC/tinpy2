import requests
import json
import tinpy
import MySQLdb
from datetime import datetime
import time
import os
from envs import *


for i in range(5):
    try:
        conn = MySQLdb.connect(user=db_username, passwd=db_pass,
                       host=db_host, db="mysql", use_unicode=True, charset="utf8mb4")
        print("connect success.")
        break
    except:
        print("connect error to DB... Try again in 3 seconds.")
        time.sleep(3)
else:
    print("Error connecting DB. system stoped.")
    sys.exit(1)

c = conn.cursor()
user_insert_stmt = 'INSERT INTO tinpy2.user(id, date, name, age, gender, distance_mi, bio, jobs, schools, matched) VALUES(%(id)s, %(date)s, %(name)s, %(age)s, %(gender)s, %(distance_mi)s, %(bio)s, %(jobs)s, %(schools)s, False);'


token = tinpy.getAccessToken(FB_email, FB_pass)
api = tinpy.API(token)
api.setLocation(latitude, longitude)

for user in api.getNearbyUsers():
    if api.getLikesRemaining() == 0:
        break
    for i, url in enumerate(user.photos):
        r = requests.get(url)
        extension = os.path.splitext(url)[-1]
        with open("/images/{0}-{1}{2}".format(user.id, i, extension), "wb") as fp:
            fp.write(r.content)

    age = user.age
    if age is None:
        age = -1
    distance_mi = user.distance_mi
    if distance_mi is None:
        distance_mi = -1
    gender = user.gender
    if gender is None:
        gender = -1
    data = {"id": user.id, "date": datetime.now(), "name": user.name, "age": age,
            "gender": gender, "distance_mi": distance_mi, "bio": user.bio, "schools": " ".join(user.schools), "jobs": " ".join(user.jobs)}
    c.execute(user_insert_stmt, data)
    user.like()
    conn.commit()

conn.close()
