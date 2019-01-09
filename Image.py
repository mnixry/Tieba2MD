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
import queue
from time import sleep
from socket import timeout
from avalon_framework import Avalon
from urllib import parse, request, error


class image():

    def __init__(self, bedKey='2333', debug=False, threadNumber=4):
        self.__accessKey = str(bedKey)
        self.__threadNumber = int(threadNumber)
        if debug == True:
            self.debug = True
        else:
            self.debug = False
        #User-Agent获取，请确保“user-agents.txt”存在
        with open('user-agents.txt', 'rt', 1, 'utf-8', 'ignore') as fileRead:
            self.__userAgent = fileRead.readlines()

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

    def bedUpload(self, raw):
        postData = {}
        imageEncoded = base64.b64encode(raw)
        if self.debug:
            Avalon.debug_info('API Access Key:%s,Image Base64:%s'%(self.__accessKey,str(imageEncoded)[0:30]))
        postData['key'] = str(self.__accessKey)
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


    def multiThread(self, imgLinkList):
        if type(imgLinkList) != list:
            raise TypeError
        self.__imageExit = False
        imageThread = []
        self.__workQueue = queue.Queue(self.__threadNumber*4)
        self.__queueLock = threading.Lock()
        for i in range(self.__threadNumber):
            thread = threading.Thread(target=fullBehavior,name='ImageThread-%d'%i,args=(self))
            thread.start()
            imageThread.append(thread)
        self.__queueLock.acquire()
        for i in imgLinkList:
            self.__workQueue.put(str(i))
        self.__queueLock.release()
        while not self.__workQueue.empty():
            pass
        self.__imageExit = True
        for i in imageThread:
            i.join(timeout=15)
        return(self.picinfo)

def fullBehavior(self):
    link = self.__workQueue
    self.picinfo = {}
    while not self.__imageExit:
        self.__queueLock.acquire()
        if not self.__workQueue.empty():
            imageOriginLink = str(link.get())
            if self.debug:
                Avalon.debug_info('Thread Start Image %s'%imageOriginLink)
            self.__queueLock.release()
            pictureRaw = image.get(self,imageOriginLink)
            pictureUpload = image.bedUpload(self,pictureRaw)
            self.picinfo[imageOriginLink] = str(pictureUpload)
        else:
            self.__queueLock.release()
        #sleep(1)