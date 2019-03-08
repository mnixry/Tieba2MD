from .valueGen import *
from .networkRequest import *
import json

def getContext(threadID:int,pageNumber:int=1,reversePost:bool=False):
    requestUrl = 'http://c.tieba.baidu.com/c/f/pb/page'
    postData = {}
    postData['_client_id'] = getAndroidStamp()
    postData['_client_type'] = '2'
    postData['_client_version'] = '9.9.8.32'
    postData['kz'] = str(threadID)
    if reversePost is True:
        postData['last'] = '1'
        postData['r'] = '1'
    else:
        postData['pn'] = str(pageNumber)
    encodedDataToSign = methodEncode(urlData=postData)
    postData['sign'] = getTiebaSign(postData=encodedDataToSign)
    gotData = methodPost(url=requestUrl,datasEncoded=methodEncode(postData))
    return json.loads(s=gotData.decode())

def getReply(threadID:int,pageNumver:int=1):
    pass