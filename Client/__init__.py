from .valueGen import *
from .networkRequest import *
import json


def getContext(threadID: int, pageNumber: int = 1, reversePost: bool = False):
    requestUrl = 'http://c.tieba.baidu.com/c/f/pb/page'
    postData = {'_client_id': getAndroidStamp(),
                '_client_type': '2',
                '_client_version': '9.9.8.32',
                'kz': str(threadID)}
    if reversePost is True:
        postData['last'] = '1'
        postData['r'] = '1'
    else:
        postData['pn'] = str(pageNumber)
    encodedDataToSign = methodEncode(urlData=postData)
    postData['sign'] = getTiebaSign(postData=encodedDataToSign)
    gotData = methodPost(url=requestUrl, datasEncoded=methodEncode(postData))
    return str(gotData.decode(errors='ignore'))


def getReply(threadID: int, replyID: int, pageNumber: int = 1):
    requestUrl = 'http://c.tieba.baidu.com/c/f/pb/floor'
    postData = {'_client_id': getAndroidStamp(),
                '_client_type': '2',
                '_client_version': '9.9.8.32',
                'kz': str(threadID),
                'pid': str(replyID),
                'pn': str(pageNumber)}
    encodedDataToSign = methodEncode(urlData=postData)
    postData['sign'] = getTiebaSign(postData=encodedDataToSign)
    gotData = methodPost(url=requestUrl, datasEncoded=methodEncode(postData))
    return str(gotData.decode(errors='ignore'))


def getUser(userName: str):
    requsetUrl = 'http://tieba.baidu.com/home/main?un=%s&fr=home' % userName
    gotData = methodGet(url=requsetUrl)
    return str(gotData.decode(errors='ignore'))


def formatJson(originData: str):
    loadedData = json.loads(originData)
    formatedData = json.dumps(loadedData, indent=4,
                              ensure_ascii=False, sort_keys=True)
    return formatedData
