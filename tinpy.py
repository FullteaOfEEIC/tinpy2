import requests
import json
import datetime
import copy
import sys
from accessToken import getAccessToken


class Person:
    def __init__(self, data):
        # jsonの値(辞書形式)を受け取ります。

        # エンドポイントです。
        self.endpoint = "https://api.gotinder.com/"

        # Tinderのサーバーの内部で使われていると思われる、ユーザー識別子です。
        self.id = data["_id"]

        # 渡されたデータそのものです。
        self.data = data

        # プロフィール文です。プロフィールが空の場合フィールド自体が存在しない???
        if "bio" in data:
            self.bio = data["bio"]
        else:
            self.bio = ""

        # 誕生日をもとに年齢を計算しています。こちらも人によってはフィールド自体が存在しません。
        if "birth_date" in data:
            birth_date = data["birth_date"]
            birth_date = datetime.datetime.strptime(
                birth_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            today = datetime.datetime.now()
            self.age = today.year - birth_date.year - \
                ((today.month, today.day) < (birth_date.month, birth_date.day))
        else:
            self.age = None

        # 性別です。男性が0, 女性が1で表されています。
        self.gender = data["gender"]

        # 名前です。
        self.name = data["name"]

        # 写真とloop videoです。サーバーからurlが送られてきます。
        # サーバーからの返り値には、オリジナルのサイズの他に様々な大きさの画像のurlが含まれていますが、正直不要なのでオリジナルの画像のurlだけを格納します。
        self.photos = []
        self.videos = []

        if "photos" in data:
            for photo in data["photos"]:
                self.photos.append(photo["url"])
                if "processedVideos" in photo:
                    self.videos.append(photo["processedVideos"][0]["url"])

        # 仕事です。空だとフィールド自体が存在しないようです。
        self.jobs = []
        if "jobs" in data:
            for job in data["jobs"]:
                if "title" in job:
                    self.jobs.append(job["title"]["name"])
                if "company" in job:
                    self.jobs.append(job["company"]["name"])

        # 学校です。空だとフィールド自体が存在しないようです。
        self.schools = []
        if "schools" in data:
            for school in data["schools"]:
                self.schools.append(school["name"])

    def __repr__(self):
        return self.name

    # 実際にサーバーにリクエストを投げる関数です。
    # headerは後ほど継承先で作成します。
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
    def __init__(self, FBtoken):
        # Facebookのトークンを元に、tinderのトークンを取得します。
        params = {"token": FBtoken}
        with requests.Session() as s:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
            s.headers.update(headers)
            response = s.post(
                "https://api.gotinder.com/v2/auth/login/facebook", data=json.dumps(params))
            if response.status_code == 401:  # 予期せぬトラブル
                sys.exit(1)
            data = json.loads(response.text)["data"]
            self.id = data["_id"]
            self.api_token = data["api_token"]
            self.refresh_token = data["refresh_token"]

        # Tinderのサーバーにリクエストするためのヘッダー。
        self.header = {"X-Auth-Token": self.api_token, "Content-type": "application/json",
                       "User-agent": "Tinder/10.1.0 (iPhone; iOS 12.1; Scale/2.00)"}

        # 自分の情報を取得します。
        meta = self.getMeta()

        # Personクラスを継承
        super().__init__(meta["user"])

        self.age_filter_max = meta["user"]["age_filter_max"]
        self.age_filter_min = meta["user"]["age_filter_min"]
        self.distance_filter = meta["user"]["distance_filter"]
        self.gender_filter = meta["user"]["gender_filter"]
        self.full_name = meta["user"]["full_name"]

    # 自分の情報を取得
    def getMeta(self):
        endpoint = "meta"
        return self._request(endpoint)

    # 周囲のユーザーを取得
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

    # idを指定するとそのユーザーを取得
    def getUser(self, id):
        endpoint = "user/{}".format(id)
        return User(self._request(endpoint, method="GET")["results"], self.header)

    # 自身のプロフィールを更新。正直アプリからやったほうが早くて楽。
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

    # 自身の位置情報を更新
    def setLocation(self, latitude, longitude):
        endpoint = "v2/meta"
        params = {"lat": latitude, "lon": longitude}
        return self._request(endpoint, method="POST", params=params)

    # マッチに関する情報と、その他よくわからない情報が格納されている
    def _updates(self, last=0):
        endpoint = "updates"
        params = {"last_activity_date": last}
        return self._request(endpoint, method="POST", params=params)

    # 上で取得した情報からマッチに関する情報だけを抜き出している
    def getMatch(self, last=0):
        results = self._updates(last)["matches"]
        return [Match(result, self.header) for result in results if "person" in result]

    # 残り右スワイプ数
    def getLikesRemaining(self):
        return int(self.getMeta()["rating"]["likes_remaining"])


class User(Person):
    def __init__(self, data, header):
        # Personクラスでリクエストを投げるために、何らかの形でヘッダーを渡さなければなりません。
        # もう少し賢く実装できないかなぁ...。
        super().__init__(data)
        self.header = header

        # 自分との距離です。
        if "distance_mi" in data:
            self.distance_mi = data["distance_mi"]
        else:
            self.distance_mi = None

        # s_number。サーバーから意味ありげに送られてきますが、なんのデータなのかさっぱりわかりません。一応保持。
        if "s_number" in data:
            self.s_number = data["s_number"]
        else:
            self.s_number = None

        # なんとなく変数名から予測がつかないこともないデータ達です。性質をしっかり検証するには課金した女性のアカウントを実験用に作成する必要がありそうなので、適当です。
        if "is_traveling" in data:
            self.is_traveling = data["is_traveling"]
        else:
            self.is_traveling = None
        if "is_tinder_u" in data:
            self.is_tinder_u = data["is_tinder_u"]
        else:
            self.is_tinder_u = None
        if "hide_age" in data:
            self.hide_age = data["hide_age"]
        else:
            self.hide_age = None
        if self.hide_age:
            self.age = None
        if "hide_distance" in data:
            self.hide_distance = data["hide_distance"]
        else:
            self.hide_distance = None
        if self.hide_distance:
            self.distance_mi = None

    # 右スワイプ
    def like(self):
        endpoint = "like/{}".format(self.id)
        return self._request(endpoint)

    #左スワイプ //passは予約語
    def nope(self):
        endpoint = "pass/{}".format(self.id)
        return self._request(endpoint)

    # スーパーライク。動かない??
    def superlike(self):
        endpoint = "like/{}/super".format(self.id)
        return self._request(endpoint, method="POST")


class Match(Person):
    def __init__(self, json, header):

        try:
            self.matchId = json["_id"]
            json.update(copy.deepcopy(json["person"]))
            super().__init__(json)
            self.header = header
            self.message_count = json["message_count"]
            if "messages" in json:
                self.messages = [Message(i) for i in json["messages"]]
            else:
                self.messages = []
        # なんかよくわからないゴミ?データがレスポンスに含まれている模様。とりあえずスルー。
        except KeyError:
            self.header = header
            pass

    #メッセージを送信
    def sendMessage(self, message):
        endpoint = "user/matches/{0}".format(self.matchId)
        params = {"message": str(message)}
        return self._request(endpoint, method="POST", params=params)


class Message:
    def __init__(self, json):
        self.id = json["_id"]
        self.match_id = json["match_id"]
        self.message = json["message"]
        self.timestamp = json["timestamp"]
        self.to = json["to"]
        self.from_ = json["from"]  # fromは予約語

    def __repr__(self):
        return self.message
