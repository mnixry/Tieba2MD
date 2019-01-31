#/usr/local/env python3
#__coding:utf-8 __
#Project Link:https://github.com/mnixry/Tieba2MD
'''
图像处理模块

遵守GPL协议，侵权必究
'''

import random
import json
import threading
import os
import uuid
from socket import timeout
from .fileUpload import MultiPartForm
from avalon_framework import Avalon
from urllib import request, error
from time import sleep
from shutil import rmtree


class image():
    def __init__(self: None, debug: bool = False,
                 workDir: str = os.getcwd(), tempDir: str = 'temp'):
        with open('user-agents.txt') as f:
            userAgents = f.readlines()
        self.__fullTempPath = os.path.join(workDir, tempDir)
        if not os.path.exists(self.__fullTempPath):
            os.mkdir(self.__fullTempPath)
        self.__getUserAgent = lambda: random.choice(
            userAgents).replace('\n', '')
        self.__getRandomUUID = lambda: uuid.uuid4().hex.upper() + '.jpg'
        self.__imageLinkDict = {}
        if debug is True:
            self.__debugMode = True
        elif debug is False:
            self.__debugMode = False
        else:
            raise TypeError

    def downloadSingleImage(self: None, imageLink: str):
        for i in range(1, 11):
            try:
                r = request.Request(imageLink)
                r.add_header('Referer', 'https://tieba.baidu.com')
                r.add_header('User-Agent', self.__getUserAgent())
                imageRes = request.urlopen(r, timeout=10).read()
            except error.URLError as e:
                Avalon.warning('图片下载失败!原因:%s[%d/10]' % (e.reason, i))
            except timeout as e:
                Avalon.warning('图片下载失败!原因:%s[%d/10]' % (e, i))
            except:
                Avalon.warning('图片下载失败!原因:未知错误[%d/10]' % i)
            else:
                break
        else:
            return(False)
        if self.__debugMode:
            Avalon.debug_info('图片下载成功!原链接:%s,文件大小:%dbytes' % (
                imageLink, len(imageRes)))
        return(imageRes)

    def uploadSingleImage(self: None, imageFilePath: str):
        form = MultiPartForm()
        with open(imageFilePath, 'rb') as f:
            form.add_file('image', f.name, f)
            form.add_field('token', '')
            form.add_field('apiSelect', 'Sina')
        r = request.Request(
            'https://image.mnixry.cn/api/v1/upload', data=bytes(form))
        r.add_header('User-Agent', self.__getUserAgent())
        r.add_header('Content-type', form.get_content_type())
        r.add_header('Content-length', len(bytes(form)))
        if self.__debugMode:
            Avalon.debug_info('文件名:%s,请求头:%s' % (
                os.path.split(imageFilePath)[1], str(r.headers)))
        for i in range(1, 11):
            try:
                uploadRes = request.urlopen(r, timeout=10).read().decode()
            except error.URLError as e:
                Avalon.warning('图片上传失败!原因:%s[%d/10]' % (e.reason, i))
            except timeout as e:
                Avalon.warning('图片上传失败!原因:%s[%d/10]' % (e, i))
            except:
                Avalon.warning('图片上传失败!原因:未知错误[%d/10]' % i)
            else:
                uploadRes = json.loads(uploadRes)
                if int(uploadRes['code']) != 200:
                    Avalon.warning('图片上传失败!原因:%s[%d/10]' %
                                   (uploadRes['msg'], i))
                    continue
                else:
                    del form
                    break
        else:
            return(False)
        if self.__debugMode:
            Avalon.debug_info('图片上传成功!图床链接:%s,本地地址:%s' % (
                uploadRes['data']['url'], imageFilePath))
        return(uploadRes['data']['url'])

    def __fullBehavior(self: None, imageOriginLink: str):
        imageResourse = self.downloadSingleImage(imageOriginLink)
        if imageResourse is False:
            self.__imageLinkDict[imageOriginLink] = imageOriginLink
        fullImagePath = os.path.join(
            self.__fullTempPath, self.__getRandomUUID())
        with open(fullImagePath, 'wb') as f:
            f.write(imageResourse)
        imageUploadLink = self.uploadSingleImage(fullImagePath)
        if imageUploadLink is False:
            self.__imageLinkDict[imageOriginLink] = imageOriginLink
        else:
            self.__imageLinkDict[imageOriginLink] = imageUploadLink
        return(imageUploadLink)

    def uploadMultiImage(self: None, imageFileList: list):
        self.__imageLinkDict.clear()
        for i in imageFileList:
            threading._start_new_thread(self.__fullBehavior, (i,))
            sleep(0.2)
        while not (len(imageFileList) == len(self.__imageLinkDict)):
            try:
                sleep(1)
            except:
                Avalon.critical('用户强制退出')
                quit(1)
        return(self.__imageLinkDict)


if __name__ == "__main__":
    Avalon.critical('模块非法调用!请运行Main.py!')
    quit(1)
