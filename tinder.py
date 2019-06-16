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
            user_id = match["person"]["_id"]
            name = match["person"]["name"]
            print("{0}:\tuser_id={1}\tmatch_id={2}".format(
                name, user_id, match_id))
        except:
            pass
