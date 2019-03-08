from urllib import request
from urllib import error
from urllib import parse
from socket import timeout
from avalon_framework import Avalon

def methodGet(url:str):
    encodedUrl = parse.urlparse(url=url)
    requestMaker = request.Request(encodedUrl)
    for tryTimes in range(10):
        try:
            dataGet = request.urlopen(url=requestMaker,timeout=10).read()
        except error.URLError as e:
            Avalon.debug('GET "%s" Failed,reason:%s,Program will Try %d Times Later.'%(url,e.reason,10-tryTimes))
        except timeout as e:
            Avalon.debug('GET "%s" Timeout,reason:%s,Program will Try %d Times Later.'%(url,e,10-tryTimes))
        except:
            Avalon.debug('GET "%s" Timeout with no reason,Program will Try %d Times Later.'%(url,10-tryTimes))
        else:
            break
    else:
        Avalon.error('GET "%s" Failed during all request,please check your network status.'%url)
        quit(1)
    return dataGet

def methodPost(url:str,dataEncoded:bytes):
    pass