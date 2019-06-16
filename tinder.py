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
        "https://api.gotinder.com/v2/auth/login/facebook?local=ja", data=json.dumps(params))
    response = json.loads(response.text)
    api_token = response["data"]["api_token"]

    # Tinderのヘッダーをセット
    headers = {"X-Auth-Token": api_token, "Content-type": "application/json",
               "User-agent": "Tinder/10.1.0 (iPhone; iOS 12.1; Scale/2.00)"}
    s.headers.update(headers)

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
