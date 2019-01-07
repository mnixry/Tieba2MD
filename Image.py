#/usr/local/env python3
#__coding:utf-8 __
'''
图像处理模块

遵守GPL协议，侵权必究
'''

import base64
import os
import random
import json
from avalon_framework import Avalon
from urllib import parse, request, error


class image():

    def __init__(self, bedKey=2333):
        #User-Agent获取，请确保“user-agents.txt”存在
        self.__accessKey = bedKey
        with open('user-agents.txt', 'rt', 1, 'utf-8', 'ignore') as fileRead:
            self.__userAgent = fileRead.readlines()

    def get(self, link):
        while True:
            try:
                imageRequest = request.Request(link)
                imageRequest.add_header(
                    'User-Agent', (random.choice(self.__userAgent)).replace('\n', ''))
                imageRequest.add_header('Referer', 'https://tieba.baidu.com')
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

    def bedUpload(self, raw):
        postData = {}
        imageEncoded = base64.b64encode(raw)
        postData['key'] = int(self.__accessKey)
        postData['OnlyUrl'] = 0
        postData['imgBase64'] = imageEncoded
        postData = parse.urlencode(postData).encode()
        while True:
            try:
                postRequest = request.Request(
                    'https://image.mnixry.cn/public/api', postData)
                postRequest.add_header(
                    'User-Agent', (random.choice(self.__userAgent)).replace('\n', ''))
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
