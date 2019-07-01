import tinpy
from tinpy import getAccessToken

FBemail = "Facebookのメールアドレス"
FBpass = "Facebookのパスワード"

token = getAccessToken(FBemail, FBpass)
api = tinpy.API(token)
api.setLocation(35.658034, 139.701636)

for user in api.getNearbyUsers():
    user.like()
