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
import threading
import uuid
import string
from time import sleep
from socket import timeout
from avalon_framework import Avalon
from urllib import parse, request, error



__randomGen = lambda l:''.join(random.choice(string.digits + string.ascii_letters) for i in range(l))
class image():

    def __init__(self, bedKey='', debug=False, threadNumber=4,workDir=os.getcwd(),tempDir='temp'):
        self.__tempDir = os.path.join(workDir,tempDir)
        self.__accessKey = str(bedKey)
        self.__threadNumber = int(threadNumber)
        if debug == True:
            self.debug = True
        else:
            self.debug = False
        #User-Agent获取，请确保“user-agents.txt”存在
        with open('user-agents.txt', 'rt', 1, 'utf-8', 'ignore') as fileRead:
            self.__userAgent = []
            for perline in fileRead.readlines():
                self.__userAgent.append(perline.replace('\n',''))

    def get(self, link):
        if self.debug:
            Avalon.debug_info('Image Link:%s'%link)
        while True:
            try:
                imageRequest = request.Request(link)
                imageRequest.add_header(
                    'User-Agent', (random.choice(self.__userAgent)).replace('\n', ''))
                imageRequest.add_header('Referer', 'https://tieba.baidu.com')
                imageRead = request.urlopen(imageRequest,timeout=5).read()
            except error.URLError as e:
                Avalon.warning('图片上传错误!原因:%s'%e.reason)
            except timeout as e:
                Avalon.warning('图片上传错误!原因:%s'%e)
            except KeyboardInterrupt:
                Avalon.error("用户强制退出")
                quit()
            except:
                Avalon.warning("出现未知错误!")
            else:
                break
        return(imageRead)

    def tempWrite(self,raw):
        if not os.path.exists(self.__tempDir):
            os.mkdir(self.__tempDir)
        tempFileName = str(uuid.uuid4()) + '.jpg'
        tempFileName = os.path.join(self.__tempDir,tempFileName)
        with open(tempFileName,'wb') as fileIO:
            fileIO.write(raw)
        return(tempFileName)

    def bedUpload(self, fileName):
        # postData = {}
        # with open(fileName,'rb') as raw:
        #     files = {'image':{'filename':os.path.split(fileName)[1].encode(),'content':raw.read(),'mimetype':'images/jpeg'}}
        # #if self.debug:
        # #    Avalon.debug_info('API Access Key:%s,Image Bytes:%s'%(self.__accessKey,str(raw)[0:30]))
        # postData['token'] = str(self.__accessKey)
        # postData['apiSelect'] = 'SouGou'
        # Reqdata,headers = encodeFilesMultipart(postData,files)
        while True:
            headers = {}
            try:
                headers['User-Agent'] = random.choice(self.__userAgent)
                #headers = parse.urlencode(headers).encode()
                # headers = {'User-Agent':random.choice(self.__userAgent)}
                postRequest = request.Request(
                     'https://image.mnixry.cn/api/v1/upload',headers=headers,data=open(fileName,'rb'))
                readRes = request.urlopen(postRequest,timeout=5).read()
            except error.URLError as e:
                Avalon.warning('图片上传出错!原因:%s'%e.reason)
            except timeout as e:
                Avalon.warning('图片上传出错!原因:%s'%e)
            except KeyboardInterrupt:
                Avalon.error("用户强制退出")
                quit()
            #except:
            #    Avalon.warning("出现未知错误!")
            else:
                readDict = json.loads(readRes.decode())
                if readDict['code'] == '200':
                    break
                else:
                    Avalon.warning('图片上传出错!原因:%s' % (str(readDict['msg'])))
        return(str(readDict['data']['url']))


    def multiThread(self, imgList):
        imgLinkList = imgList
        self.picinfo = {}
        if type(imgLinkList) != list or list(imgLinkList) == []:
            raise TypeError
        for i in imgLinkList:
            threading._start_new_thread(image.fullBehavior,(self,i))
        while True:
            for i in imgLinkList:
                if self.picinfo.get(i) != None:
                    imgLinkList.remove(i)
            if imgLinkList == []:
                break
        return(self.picinfo)

    def fullBehavior(self,link):
        imgOrigin = str(link)
        imgResourse = image.get(self,imgOrigin)
        imgFilename = image.tempWrite(self,imgResourse)
        imgUp = image.bedUpload(self,imgFilename)
        self.picinfo[imgOrigin] = imgUp
        return()


def encodeFilesMultipart(data, files):
    boundary = __randomGen(30)
    special_separator = "--" + boundary
    lines = []

    for name, value in data.items():
        lines.extend((
            special_separator,
            'Content-Disposition: form-data; name="%s"' % str(name),
            '',
            str(value.encode()),
        ))

    for name, value in files.items():
        filename = value["filename"]
        lines.extend((
            special_separator,
            'Content-Disposition: form-data; name="%s"; filename="%s"' % (
                str(name), str(filename)),
            'Content-Type: %s' % value["mimetype"],
            'Content-Transfer-Encoding: binary',
            '',
            str(value['content']),
        ))

    lines.extend((
        special_separator + "--",
        '',
    ))
    body = '\r\n'.join(lines)

    headers = {
        'Content-Type': 'multipart/form-data; boundary=%s' % boundary,
        'Content-Length': str(len(body)),
    }

    return (body, headers)
