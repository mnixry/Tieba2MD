from urllib import request
from urllib import error
from urllib import parse
from socket import timeout
from avalon_framework import Avalon

def methodGet(url:str,headers:dict={},maxTryTimes:int=10):
    encodedUrl = parse.urlparse(url=url).geturl()
    requestMaker = request.Request(encodedUrl,headers=headers)
    for tryTimes in range(maxTryTimes):
        try:
            dataGet = request.urlopen(url=requestMaker,timeout=10).read()
        except error.URLError as e:
            Avalon.debug('GET "%s" Failed,reason:%s,Program will Try %d Times Later.'%(url,e.reason,maxTryTimes-tryTimes))
        except timeout as e:
            Avalon.debug('GET "%s" Timeout,reason:%s,Program will Try %d Times Later.'%(url,e,maxTryTimes-tryTimes))
        except:
            Avalon.debug('GET "%s" Timeout with no reason,Program will Try %d Times Later.'%(url,maxTryTimes-tryTimes))
        else:
            break
    else:
        Avalon.error('GET "%s" Failed during all request,please check your network status.'%url)
        quit(1)
    return dataGet

def methodPost(url:str,datasEncoded:bytes,headers:dict={},maxTryTimes:int=10):
    encodedUrl = parse.urlparse(url=url).geturl()
    requsetMaker = request.Request(url=encodedUrl,headers=headers,data=datasEncoded)
    for tryTimes in range(maxTryTimes):
        try:
            dataPost = request.urlopen(url=requsetMaker,timeout=10).read()
        except error.URLError as e:
            Avalon.debug('POST "%s" Failed,reason:%s,Program will Try %d Times Later.'%(url,e.reason,maxTryTimes-tryTimes))
        except timeout as e:
            Avalon.debug('POST "%s" Timeout,reason:%s,Program will Try %d Times Later.'%(url,e,maxTryTimes-tryTimes))
        except:
            Avalon.debug('POST "%s" Timeout with no reason,Program will Try %d Times Later.'%(url,maxTryTimes-tryTimes))
        else:
            break
    else:
        Avalon.error('POST "%s" Failed during all request,please check your network status.'%url)
        quit(1)
    return dataPost

def methodEncode(urlData:dict):
    return parse.urlencode(query=urlData).encode()