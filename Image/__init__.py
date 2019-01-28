#/usr/local/env python3
#__coding:utf-8 __
#Project Link:https://github.com/mnixry/Tieba2MD
'''
图像处理模块

遵守GPL协议，侵权必究
'''

import random,json,threading,os,uuid
from .fileUpload import MultiPartForm
from avalon_framework import Avalon
from urllib import request,error
from time import sleep


class image():
    def __init__(self,debug=False,workDir=os.getcwd(),tempDir='temp'):
        with open('user-agents.txt') as f:
            userAgents = f.readlines()
        self.__fullTempPath = os.path.join(workDir,tempDir)
        if not os.path.exists(self.__fullTempPath):
            os.mkdir(self.__fullTempPath)
        self.__getUserAgent = lambda:random.choice(userAgents).replace('\n','')
        self.__getRandomUUID = lambda:uuid.uuid4().hex.upper() + '.jpg'
        self.__imageLinkList = []
        if debug is True:
            self.__debugMode = True
        elif debug is False:
            self.__debugMode = False
        else:
            raise TypeError

    def downloadSingleImage(self,imageLink:str):
        while True:
            try:
                r = request.Request(imageLink)
                r.add_header('Referer','https://tieba.baidu.com')
                r.add_header('User-Agent',self.__getUserAgent())
                imageRes = request.urlopen(r,timeout=10).read()
            except error.URLError as e:
                Avalon.warning('Image Download Error!Message:%s'%e.reason)
            except:
                Avalon.warning('Image Upload Error!Unknown Error!')
            else:
                break
        if self.__debugMode:
            Avalon.debug_info('Image Download Success!Link:%s,Length:%d'%(imageLink,len(imageRes)))
        return(imageRes)

    def uploadSingleImage(self,imageFilePath:str):
        form = MultiPartForm()
        form.add_field('apiSelect','SouGou')
        form.add_field('token','')
        with open(imageFilePath,'rb') as f:
            form.add_file('image',os.path.split(imageFilePath)[1],f)
        r = request.Request('https://image.mnixry.cn/api/v1/upload',data=bytes(form))
        r.add_header('User-Agent',self.__getUserAgent())
        r.add_header('Content-type',form.get_content_type())
        r.add_header('Content-length',len(bytes(form)))
        while True:
            try:
                uploadRes = request.urlopen(r,timeout=10).read().decode()
            except error.URLError as e:
                Avalon.warning('Image Upload Error!Message:%s'%e.reason)
            except:
                Avalon.warning('Image Upload Error!Unknown Error!')
            else:
                uploadRes = json.loads(uploadRes)
                if int(uploadRes['code']) != 200:
                    Avalon.warning('Image Upload Error!Message:%s'%uploadRes['msg'])
                    continue
                else:
                    break
        del form
        if self.__debugMode:
            Avalon.debug_info('Image Upload Success!Link:%s,Origin Path:%s'%(uploadRes['data']['url'],imageFilePath))
        self.__imageLinkList.append(uploadRes['data']['url'])
        return(uploadRes['data']['url'])

    def __fullBehavior(self,imageOriginLink:str):
        imageResourse = self.downloadSingleImage(imageOriginLink)
        fullImagePath = os.path.join(self.__fullTempPath,self.__getRandomUUID())
        with open(fullImagePath,'wb') as f:
            f.write(imageResourse)
        imageUploadLink = self.uploadSingleImage(fullImagePath)
        return(imageUploadLink)

    def uploadMultiImage(self,imageFileList:list):
        self.__imageLinkList.clear()
        for i in imageFileList:
            threading._start_new_thread(self.__fullBehavior,(i,))
        while not (len(imageFileList) == len(self.__imageLinkList)):
            sleep(1)
        returnList = self.__imageLinkList
        self.__imageLinkList.clear()
        return(returnList)