#/usr/local/env python3
#__coding:utf-8 __
'''
图像处理模块

遵守GPL协议，侵权必究
'''

import base64,os,random,json
from avalon_framework import Avalon
from urllib import parse,request,error

_userAgent = (open('user-agents.txt','rt',1,'utf-8','ignore')).readlines()

class image():
    
    def get(link):
        while True:
            try:
                imageRequest = request.Request(link)
                imageRequest.add_header('User-Agent',(random.choice(_userAgent)).replace('\n',''))
                imageRequest.add_header('Referer','https://tieba.baidu.com')
                imageRead = request.urlopen(imageRequest).read()
            except error.URLError as e:
                Avalon.warning('图片上传错误!原因:%s' % (str(e)))
            except KeyboardInterrupt:
                Avalon.error("用户强制退出")
                quit()
            except:
                Avalon.warning("出现未知错误!")
            else:
                break
        return(imageRead)

    def bedUpload(raw):
        postData = {}
        imageEncoded = base64.b64encode(raw)
        postData['key'] = 2333
        postData['OnlyUrl'] = 0
        postData['imgBase64'] = imageEncoded
        postData = parse.urlencode(postData).encode()
        while True:
            try:
                postRequest = request.Request('https://image.mnixry.cn/public/api',postData)
                postRequest.add_header('User-Agent',(random.choice(_userAgent)).replace('\n',''))
                readRes = request.urlopen(postRequest).read()
            except error.URLError as e:
                Avalon.warning('图片上传出错!原因:%s' % (str(e)))
            except KeyboardInterrupt:
                Avalon.error("用户强制退出")
                quit()
            except:
                Avalon.warning("出现未知错误!")
            else:
                readDict = json.loads(readRes.decode())
                if readDict['code'] == '1':
                    break
                else:
                    Avalon.warning('图片上传出错!原因:%s' % (str(readDict['msg'])))
        return(str(readDict['img']))