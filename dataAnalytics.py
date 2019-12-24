import shelve
import requests
import numpy as np
import cv2
import subprocess
import MeCab
import pandas as pd

cmd = 'echo `mecab-config --dicdir`"/mecab-ipadic-neologd"'
path = (subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         shell=True).communicate()[0]).decode('utf-8')
m = MeCab.Tagger("-d {0}".format(path))
m_wakati = MeCab.Tagger("-d {0} -Owakati".format(path))

sf = shelve.open("data/models/models.db")
clf = sf["clf_final"]
doc2vec = sf["doc2vec"]
TheilSen = sf["bio_TheilSen"]
rf = sf["bio_rf"]
xgb = sf["bio_xgb"]
mlp = sf["bio_mlp"]
VGG = sf["VGG16_based"]


def getPhotos(url):
    img = requests.get(url).content
    img = np.frombuffer(img, np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (120, 120))
    return img


def getPhotoScore(user, models):
    imgs = np.asarray([getPhotos(url) for url in user.photos])
    scores = []
    for model in models:
        scores.append(model.predict(imgs))
    scores = np.asarray(scores)
    scores = np.mean(scores, axis=0)
    return np.mean(scores), np.max(scores)


def getBioScore(user, doc2vec, mlp, xgb, rf, TheilSen):
    vector = doc2vec.infer_vector(m_wakati.parse(
        str(user.bio)).split(" ")).reshape(1, -1)
    mlpScore = np.mean([model.predict(vector) for model in mlp])
    xgbScore = np.mean([model.predict(vector) for model in xgb])
    rfScore = np.mean([model.predict(vector) for model in rf])
    TheilSenScore = np.mean([model.predict(vector) for model in TheilSen])
    return mlpScore, xgbScore, rfScore, TheilSenScore


def _getScore(user, clf, doc2vec, mlp, xgb, rf, TheilSen, VGG):
    df = pd.DataFrame(index=[0])
    age = (user.age - 18) / 10
    df["age"] = age
    photo_num = len(user.photos) / 6
    df["photo_num"] = photo_num
    bio_mlp, bio_xgb, bio_rf, bio_TheilSen = getBioScore(
        user, doc2vec, mlp, xgb, rf, TheilSen)
    df["bio_TheilSen"] = bio_TheilSen
    df["bio_xgb"] = bio_xgb
    bio_length = np.log1p(len(str(user.bio)))
    df["bio_length"] = bio_length
    df["bio_rf"] = bio_rf
    df["bio_mlp"] = bio_mlp
    photo_mean, photo_max = getPhotoScore(user, VGG)
    df["photo_mean"] = photo_mean
    df["photo_max"] = photo_max
    return clf.predict(df)[0]


def getScore(user):
    return _getScore(user, clf, doc2vec, mlp, xgb, rf, TheilSen, VGG)
