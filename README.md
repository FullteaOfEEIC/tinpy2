# tinpy2
Tinderを自動化するプロジェクトです。

Qiitaにて気ままに連載中...  
第1話: https://qiita.com/Fulltea/items/fe4d4214552476c28e88  
第2話: https://qiita.com/Fulltea/items/4083c75f74e8a78a797b  
第3話: https://qiita.com/Fulltea/items/aab00dba8daecb71f1e4  
第3.5話: https://qiita.com/Fulltea/items/b1d0b26e5a6ae3f3a5fb  

## Usage

```
import tinpy
from tinpy import getAccessToken

FBemail = "Facebook e-mail address"
FBpass = "Facebook password"

token = getAccessToken(FBemail, FBpass)
api = tinpy.API(token)
api.setLocation(35.658034, 139.701636)

for user in api.getNearbyUsers():
    user.like()
```
