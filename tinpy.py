import requests
import json
import datetime
import copy

class Person:
    def __init__(self, data):
        #jsonの値(辞書形式)を受け取ります。

        #エンドポイントです。
        self.endpoint = "https://api.gotinder.com/"

        #Tinderのサーバーの内部で使われていると思われる、ユーザー識別子です。
        self.id = data["_id"]

        #渡されたデータそのものです。
        self.data = data

        #プロフィール文です。プロフィールが空の場合フィールド自体が存在しない???
        if "bio" in data:
            self.bio = data["bio"]
        else:
            self.bio = ""

        #誕生日をもとに年齢を計算しています。こちらも人によってはフィールド自体が存在しません。
        if "birth_date" in data:
            birth_date = data["birth_date"]
            birth_date = datetime.datetime.strptime(
                birth_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            today = datetime.datetime.now()
            self.age = today.year - birth_date.year - \
                ((today.month, today.day) < (birth_date.month, birth_date.day))
        else:
            self.age = None

        #性別です。男性が0, 女性が1で表されています。
        self.gender = data["gender"]

        #名前です。
        self.name = data["name"]

        #写真とloop videoです。サーバーからurlが送られてきます。
        #サーバーからの返り値には、オリジナルのサイズの他に様々な大きさの画像のurlが含まれていますが、正直不要なのでオリジナルの画像のurlだけを格納します。
        self.photos = []
        self.videos = []

        if "photos" in data:
            for photo in data["photos"]:
                self.photos.append(photo["url"])
                if "processedVideos" in photo:
                    self.videos.append(photo["processedVideos"][0]["url"])

        #仕事です。空だとフィールド自体が存在しないようです。
        self.jobs = []
        if "jobs" in data:
            for job in data["jobs"]:
                self.jobs.append(job["title"]["name"])

        #学校です。空だとフィールド自体が存在しないようです。
        self.schools = []
        if "schools" in data:
            for school in data["schools"]:
                self.schools.append(school["name"])


    def __repr__(self):
        return self.name

    #実際にサーバーにリクエストを投げる関数です。
    #headerは後ほど継承先で作成します。
    def _request(self, endpoint, method="GET", params=None):
        url = "https://api.gotinder.com/" + endpoint
        with requests.Session() as s:
            s.headers.update(self.header)
            if method == "GET":
                response = s.get(url, params=params)
            elif method == "POST":
                response = s.post(url, data=json.dumps(params))
            elif method == "DELETE":
                response = s.delete(url, data=json.dumps(params))
            content = response.content
            if len(content) > 0:
                content = content.decode("utf-8")
                content = json.loads(content)

            return content


class API(Person):
    def __init__(self, token):
        params = {"token": token}
        with requests.Session() as s:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
            s.headers.update(headers)
            response = s.post(
                "https://api.gotinder.com/v2/auth/login/facebook", data=json.dumps(params))
            if response.status_code == 401:
                raise NoAuthError
            data = json.loads(response.text)["data"]
            self.id = data["_id"]
            self.api_token = data["api_token"]
            self.refresh_token = data["refresh_token"]
            self.header = {"X-Auth-Token": self.api_token, "Content-type": "application/json",
                           "User-agent": "Tinder/10.1.0 (iPhone; iOS 12.1; Scale/2.00)"}

        meta = self.getMeta()
        super().__init__(meta["user"])
        self.age_filter_max = meta["user"]["age_filter_max"]
        self.age_filter_min = meta["user"]["age_filter_min"]
        self.distance_filter = meta["user"]["distance_filter"]
        self.gender_filter = meta["user"]["gender_filter"]  # Male:0 Female:1
        self.full_name = meta["user"]["full_name"]

    def getMeta(self):
        endpoint = "meta"
        return self._request(endpoint)

    def getNearbyUsers(self, limit=10):
        endpoint = "user/recs"
        params = {"limit": limit}
        while True:
            results = self._request(endpoint, method="POST",
                                    params=params)["results"]
            if len(results) == 0:
                break

            for result in results:
                yield User(result, self.header)

    def getUser(self, id):
        endpoint = "user/{}".format(id)
        return User(self._request(endpoint, method="GET")["results"], self.header)

    def setProfile(self, Gender=None, age_filter_min=None, age_filter_max=None, distance_filter=None):
        endpoint = "profile"
        params = {}
        if Gender:
            params["Gender"] = Gender  # 0:Male 1:Female
        if age_filter_min:
            params["age_filter_min"] = age_filter_min
        if age_filter_max:
            params["age_filter_max"] = age_filter_max
        if distance_filter:
            params["distance_filter"] = distance_filter

        return self._request(endpoint, params=params, method="POST")

    def setLocation(self, latitude, longitude):
        endpoint = "v2/meta"
        params = {"lat": latitude, "lon": longitude}
        return self._request(endpoint, method="POST", params=params)

    def _updates(self, last=0):
        endpoint = "updates"
        params = {"last_activity_date": last}
        return self._request(endpoint, method="POST", params=params)

    def getMatch(self, last=0):
        results = self._updates(last)["matches"]
        return [Match(result, self.header) for result in results if "person" in result]

    def getMeta(self):
        endpoint = "meta"
        return self._request(endpoint)

    def getLikesRemaining(self):
        return int(self.getMeta()["rating"]["likes_remaining"])
