import random
import hashlib
import time
from urllib import parse
from .networkRequest import methodGet


def getAndroidStamp():
    def getDigit(d):
        return ''.join(str(random.choice(range(10))) for _ in range(int(d)))

    fullStamp = 'wappc_%s_%s' % (getDigit(13), getDigit(3))
    return fullStamp


def getTiebaSign(postData: bytes):
    decodedData = parse.unquote(string=postData.decode())
    decodedData = decodedData.replace('&', '') + 'tiebaclient!!!'
    return getMD5(decodedData.encode())


def getMD5(data: bytes):
    md5Algorithm = hashlib.md5()
    md5Algorithm.update(data)
    return md5Algorithm.hexdigest()
