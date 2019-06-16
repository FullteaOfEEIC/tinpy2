from accessToken import getAccessToken
import requests
import json

FBemail = "Facebookのメールアドレス"
FBpass = "Facebookのパスワード"


def lambda_handler(event, context):
    # FBトークンの取得
    token = getAccessToken(FBemail, FBpass)

    # Tinderのトークンの取得
    with requests.Session() as s:
        params = {"token": token}
        response = s.post(
            "https://api.gotinder.com/v2/auth/login/facebook?local=ja", data=json.dumps(params))
        response = json.loads(response.text)
        api_token = response["data"]["api_token"]

        # Tinderのヘッダーをセット
        headers = {"X-Auth-Token": api_token, "Content-type": "application/json",
                   "User-agent": "Tinder/10.1.0 (iPhone; iOS 12.1; Scale/2.00)"}
        s.headers.update(headers)

        # 位置情報の登録
        location = {"lat": 35.658034, "lon": 139.701636}  # 渋谷スクランブル交差点
        ping = s.post("https://api.gotinder.com/v2/meta",
                      params=json.dumps(params))

        likes_remaining = True
        while likes_remaining:
            # 周囲のユーザーを取得
            users = s.post("https://api.gotinder.com/user/recs")
            for user in json.loads(users.text)["results"]:
                id = user["_id"]
                # 右スワイプ
                like = s.get("https://api.gotinder.com/like/{}".format(id))
                like = json.loads(like.text)
                # スワイプの残りがなくなったら終了
                if like["likes_remaining"] == 0:
                    likes_remaining = False

        # マッチを取得
        matches = s.post("https://api.gotinder.com/updates",
                         data=json.dumps({"last_activity_date": 0}))
        matches = json.loads(matches.text)["matches"]
        for match in matches:
            try:
                match_id = match["id"]
                name = match["person"]["name"]
                messages = match["messages"]
                if len(messages) == 0:
                    s.post("https://api.gotinder.com/user/matches/{0}".format(
                        match_id), data=json.dumps({"はじめまして{0}さん！\nマッチありがとうございます！".format(name)}))
            except:
                pass
