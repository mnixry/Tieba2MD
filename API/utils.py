from functools import wraps
from hashlib import md5
from logging import getLogger
from random import randint
from time import time
from urllib import parse

_TIMER_LOGGER = getLogger('timer')


def Timeit(function: callable):
    beginTime = time() * 1000

    @wraps(function)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)

    endTime = time() * 1000
    timeDiff = round(endTime - beginTime, 3)
    _TIMER_LOGGER.debug(f'Function {function} running cost {timeDiff} ms.')
    return wrapper


@Timeit
def randomStamp():
    genDigitString = lambda d: ''.join([str(randint(0, 9)) for _ in range(d)])
    return f'wappc_{genDigitString(13)}_{genDigitString(3)}'


@Timeit
def generateSignature(postData: str) -> str:
    dataWithEncoding: str = parse.unquote(string=postData)
    signedData: str = dataWithEncoding.replace('&', '') + 'tiebaclient!!!'
    return md5(signedData.encode()).hexdigest()
