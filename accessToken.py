import re
import robobrowser
import time
import sys


def getAccessToken(email, password):

    MOBILE_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C153 Safari/604.1"
    FB_AUTH = "https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&client_id=464891386855067&ret=login&fallback_redirect_uri=221e1158-f2e9-1452-1a05-8983f99f7d6e&ext=1556057433&hash=Aea6jWwMP_tDMQ9y"
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
    s.submit_form(f, submit=f.submit_fields['__CONFIRM__'])
    # get access token from the html response
    access_token = re.search(
        r"access_token=([\w\d]+)", s.response.content.decode()).groups()[0]

    return access_token


if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 3:
        print("Usage: accessToken.py email password")
        sys.exit(1)
    email = sys.argv[1]
    password = sys.argv[2]
    print(getAccessToken(email, password))
