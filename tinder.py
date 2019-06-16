from accessToken import getAccessToken
import requests
import json

FBemail = "Facebookのメールアドレス"
FBpass = "Facebookのパスワード"

# FBトークンの取得
token = getAccessToken(FBemail, FBpass)

# Tinderのトークンの取得
with requests.Session() as s:
    params = {"token": token}
    response = s.post(
        "https://api.gotinder.com/v2/auth/login/facebook", data=json.dumps(params))
    response = json.loads(response.text)
    api_token = response["data"]["api_token"]

    # Tinderのヘッダーをセット
    headers = {"X-Auth-Token": api_token, "Content-type": "application/json",
               "User-agent": "Tinder/10.1.0 (iPhone; iOS 12.1; Scale/2.00)"}
    s.headers.update(headers)

    # 位置情報の登録
    location = {"lat": 35.658034, "lon": 139.701636}
    s.post("https://api.gotinder.com/v2/meta",
           params=json.dumps(params))

    while True:
        # 周囲のユーザーを取得
        users = s.post("https://api.gotinder.com/user/recs")
        for user in json.loads(users.text)["results"]:
            id = user["_id"]
            # 右スワイプ
            s.get("https://api.gotinder.com/like/{}".format(id))
