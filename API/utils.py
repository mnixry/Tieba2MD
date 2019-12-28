from functools import wraps
from hashlib import md5
from logging import getLogger
from random import randint
from time import time
from urllib import parse
from typing import List

_TIMER_LOGGER = getLogger('timer')


def Timeit(function: callable):
    @wraps(function)
    def wrapper(*args, **kwargs):
        beginTime = time()
        execResult = function(*args, **kwargs)
        _TIMER_LOGGER.debug(
            f'Function {function} running cost {round((time() - beginTime)*1000,3)} ms.'
        )
        return execResult

    return wrapper


def randomStamp():
    genDigitString = lambda d: ''.join([str(randint(0, 9)) for _ in range(d)])
    return f'wappc_{genDigitString(13)}_{genDigitString(3)}'


def generateSignature(postData: str) -> str:
    dataWithEncoding: str = parse.unquote(string=postData)
    signedData: str = dataWithEncoding.replace('&', '') + 'tiebaclient!!!'
    return md5(signedData.encode()).hexdigest().upper()


@Timeit
def autoType(data: dict) -> dict:
    def f(data):
        assert isinstance(data, dict)
        newData = dict(data)
        for perKey in data:
            perKey: str
            value = data[perKey]
            if isinstance(value, str):
                if value.isdigit():
                    newData[perKey] = int(value)
            elif isinstance(value, dict):
                newData[perKey] = f(value)
            elif isinstance(value, list):
                newData[perKey] = [(f(i) if isinstance(i, dict) else i)
                                   for i in value]
        return newData

    return f(data)