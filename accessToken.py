import re
import robobrowser

"""
注釈(English follows)

極めて汚いコードです。
tinderにログインする際に、```s.submit_form(f, submit=f.submit_fields['__CONFIRM__'])```を実行するとエラーが発生しますが、そのエラーメッセージの中にaccess tokenが含まれています。そのため、意図的にエラーを発生させて、そこからトークンを取得しています。
現在このコードは問題なく動いていますが、お世辞にもいいとは言えないコードですので、修正できる方がいらっしゃいましたらPRをおねがいします。


Notes.

THIS CODE IS WRITTEN IN VERY VERY BAD MANNER.
```s.submit_form(f, submit=f.submit_fields['__CONFIRM__'])``` returns error and the error message contains the access token. So I make them raise error on purpose and get token from there.
As this code works, I' m now using this and also understand that this is very bad code. If anyone could help me, please make PR.

"""



def getAccessToken(email, password):

    MOBILE_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C153 Safari/604.1"
    FB_AUTH = "https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash=AeZqkIcf-NEW6vBd"

    s = robobrowser.RoboBrowser(
        user_agent=MOBILE_USER_AGENT, parser="html.parser")
    s.open(FB_AUTH)
    # submit login form
    f = s.get_form()
    f["email"] = email
    f["pass"] = password

    s.submit_form(f)
    # click the 'ok' button on the dialog informing you that you have already authenticated with the Tinder app
    f = s.get_form()
    try:
        s.submit_form(f, submit=f.submit_fields['__CONFIRM__'])
    except Exception as e:
        errormessage=str(e)
    # get access token from the html response
        access_token = re.search(
            r"access_token=([\w\d]+)", errormessage).groups()[0]

        return access_token


if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 3:
        print("Usage: accessToken.py email password")
        sys.exit(1)
    email = sys.argv[1]
    password = sys.argv[2]
    print(getAccessToken(email, password))
