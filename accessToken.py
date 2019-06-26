import re
import robobrowser
from bs4 import BeautifulSoup
import requests
import time
import sys

#"""
def getAccessToken(email, password):
    FB_AUTH = "https://www.facebook.com/login.php?skip_api_login=1&api_key=464891386855067&kid_directed_site=0&app_id=464891386855067&signed_next=1&next=https%3A%2F%2Fwww.facebook.com%2Fv2.8%2Fdialog%2Foauth%3Fapp_id%3D464891386855067%26channel_url%3Dhttps%253A%252F%252Fstaticxx.facebook.com%252Fconnect%252Fxd_arbiter.php%253Fversion%253D44%2523cb%253Df3fbdfb8e54d14c%2526domain%253Dtinder.com%2526origin%253Dhttps%25253A%25252F%25252Ftinder.com%25252Ff3017f04f989f3c%2526relation%253Dopener%26client_id%3D464891386855067%26display%3Dpopup%26domain%3Dtinder.com%26e2e%3D%257B%257D%26fallback_redirect_uri%3Dhttps%253A%252F%252Ftinder.com%252F%26locale%3Dja_JP%26origin%3D1%26redirect_uri%3Dhttps%253A%252F%252Fstaticxx.facebook.com%252Fconnect%252Fxd_arbiter.php%253Fversion%253D44%2523cb%253Df247314c2ec0694%2526domain%253Dtinder.com%2526origin%253Dhttps%25253A%25252F%25252Ftinder.com%25252Ff3017f04f989f3c%2526relation%253Dopener%2526frame%253Df32630633c95a9%26response_type%3Dtoken%252Csigned_request%26scope%3Duser_birthday%252Cuser_photos%252Cemail%252Cuser_friends%252Cuser_likes%26sdk%3Djoey%26version%3Dv2.8%26ret%3Dlogin%26fbapp_pres%3D0%26logger_id%3Df4b8f869-06c6-44c6-ad74-5910383fd32e&cancel_url=https%3A%2F%2Fstaticxx.facebook.com%2Fconnect%2Fxd_arbiter.php%3Fversion%3D44%23cb%3Df247314c2ec0694%26domain%3Dtinder.com%26origin%3Dhttps%253A%252F%252Ftinder.com%252Ff3017f04f989f3c%26relation%3Dopener%26frame%3Df32630633c95a9%26error%3Daccess_denied%26error_code%3D200%26error_description%3DPermissions%2Berror%26error_reason%3Duser_denied&display=popup&locale=ja_JP"
    data={"email":email,"pass":password}
    with requests.Session() as s:
        #ログイン画面へ
        response=s.get(FB_AUTH)

        #ログインフォームの送信先URLを取得
        soup=BeautifulSoup(response.text,"html.parser")
        action=soup.form.get("action")
        action="https://www.facebook.com/"+action

        #ログインフォームを送信
        response=s.post(action,data=data)

        #返り値からtokenを取得
        access_token = re.search(
            r"access_token=([\w\d]+)", response.text).groups()[0]
    return access_token


if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 3:
        print("Usage: accessToken.py email password")
        sys.exit(1)
    email = sys.argv[1]
    password = sys.argv[2]
    print(getAccessToken(email, password))
