import requests
import json
import tinpy

FBemail = "Facebookのメールアドレス"
FBpass = "Facebookのパスワード"
url = "GASのURL"
#token = tinpy.getAccessToken(FBemail, FBpass)
token = "Facebookのアクセストークン"


def lambda_handler(event, context):

    api = tinpy.API(token)

    api.setLocation(35.658034, 139.701636)

    for user in api.getNearbyUsers():
        if api.getLikesRemaining() == 0:
            break
        user.like()
        sendProfile(user)

    for match in api.getMatch():
        sendMatch(match)
        messages = match.messages
        if len(messages) == 0:
            match.sendMessage(
                "はじめまして{0}さん！ マッチありがとうございます！".format(match.name))


def sendProfile(user):
    data = {"id": user.id, "name": user.name,
            "age": user.age, "gender": user.gender}
    data["bio"] = user.bio
    for i in range(len(user.photos)):
        data["photo{0}".format(i)] = user.photos[i]
    data["videos"] = user.videos
    data["schools"] = user.schools
    data["jobs"] = user.jobs
    data["distance_mi"] = user.distance_mi
    with requests.Session() as s:
        s.post(url, data=data)


def sendMatch(match):
    with requests.Session() as s:
        data = {"id": match.id}
        s.get(url, params=data)
