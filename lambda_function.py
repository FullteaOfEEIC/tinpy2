from accessToken import getAccessToken
import requests
import json
import tinpy

FBemail = "Facebookのメールアドレス"
FBpass = "Facebookのパスワード"


def lambda_handler(event, context):
    # FBトークンの取得
    token = getAccessToken(FBemail, FBpass)

    api = tinpy.API(token)

    api.setLocation(35.658034, 139.701636)

    for user in api.getNearbyUsers():
        user.like()
        if api.getLikesRemaining() == 0:
            break

    for match in api.getMatch():
        messages = match.messages
        if len(messages) == 0:
            match.sendMessage("はじめまして{0}さん！\nマッチありがとうございます！".format(match.name))
