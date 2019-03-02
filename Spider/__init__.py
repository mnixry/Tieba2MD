# /usr/local/env python3
# __coding:utf-8 __
# Project Link:https://github.com/mnixry/Tieba2MD
'''
百度贴吧帖子下载/处理模块
版本：1.4

遵守GPL协议，侵权必究
'''
from lxml import etree
from avalon_framework import Avalon
from urllib import request, error
from socket import timeout
from functools import wraps
from .fileTempSave import temp
import os
import time
import json
import random
import html


class spider():
    def __init__(self: None, postID: int, seeLZ: bool, debug: bool = False):
        self.__tempSave = temp(postID=postID)
        if seeLZ:
            self.__postLink = 'https://tieba.baidu.com/p/%s?see_lz=1&ajax=1&pn=' % (
                postID)
            #Avalon.info('模式:只看楼主', highlight=True)
        else:
            self.__postLink = 'https://tieba.baidu.com/p/%s?ajax=1&pn=' % (
                postID)
            #Avalon.info('模式:全部', highlight=True)
        # User-Agent获取，请确保“user-agents.txt”存在
        with open('user-agents.txt', 'rt', errors='ignore') as fileRead:
            self.__userAgent = fileRead.readlines()
        if debug is True:
            self.debug = True
        elif debug is False:
            self.debug = False
        else:
            raise TypeError

    def getPost(self: None, pageNumber: int, ajax: bool = True, useTemp: bool = True):  # 获得html源文件函数
        self.__workPageNumber = pageNumber
        link = self.__postLink + str(pageNumber)
        existTemp = self.__tempSave.getSameTemp()
        if existTemp.get('html') and useTemp:
            for i in existTemp['html']:
                if int(i[1]) == int(pageNumber):
                    Avalon.debug_info('第%d页已经在临时文件中存在,跳过' % pageNumber)
                    return self.__tempSave.readFileByID(i)
        if ajax is False:
            link = link.replace('ajax=1&', '')
        for tryTimes in range(1, 11):
            try:
                postRequest = request.Request(link)
                try:
                    # 设置程序请求头，伪装爬虫（必要性存疑）
                    postRequest.add_header(
                        'User-Agent', (random.choice(self.__userAgent)).replace('\n', ''))
                    postRequest.add_header(
                        'Referer', 'https://tieba.baidu.com')
                except:
                    continue
                else:
                    postRead: bytes = request.urlopen(
                        postRequest, timeout=5).read()
                    if self.debug:
                        Avalon.debug_info('链接:"%s"请求头:%s.' %
                                          (link, postRequest.headers))
            # 错误处理
            except error.URLError as e:
                Avalon.warning("获取帖子正文失败!原因:%s(%s/10)" %
                               (str(e.reason), str(tryTimes)))
            except timeout as e:
                Avalon.warning("获取帖子正文失败!原因:%s(%s/10)" %
                               (str(e), str(tryTimes)))
            except KeyboardInterrupt:
                Avalon.critical("用户强制退出")
                quit(1)
            except:
                Avalon.warning("获取帖子正文失败!原因:未知错误(%s/10)" % tryTimes)
            # 没有错误，结束循环
            else:
                if self.debug:
                    Avalon.debug_info('Link %s Get Successed.' % link)
                break
        else:
            Avalon.error('获取失败!')
            if self.debug:
                Avalon.debug('Link:%s' % link)
            quit(1)
        if useTemp is True:
            self.__tempSave.savePostRaw(postRead.decode(
                errors='ignore'), pageNumber=pageNumber)
        return(postRead.decode(errors='ignore'))

    def getPostInfo(self: None):
        postRaw = self.getPost(pageNumber=1, ajax=False, useTemp=False)
        postGet = etree.HTML(postRaw)
        postTitle = postGet.xpath('//div[@class="wrap2"]//h3/@title')
        postAuthor = postGet.xpath(
            '//div[@class="p_postlist"]/div[@class][1]//div/@author')
        postPageNum = postGet.xpath(
            '//div/div[@id]//div[@id]//li/span[@class="red"][last()]/text()')
        if not(postTitle and postAuthor and postPageNum):
            Avalon.critical('程序无法正确获得帖子信息')
            quit(1)
        finalInfo = {'Author': str(postAuthor[0]), 'Title': str(
            postTitle[0]), 'TotalPage': int(postPageNum[0])}
        self.postInfo = finalInfo
        if self.debug:
            Avalon.debug_info(self.postInfo)
        return finalInfo

    def proccessPost(self: None, raw: str, useTemp: bool = True):
        # 将源文件转换为dict类型的数据
        # 如果你没有读过百度贴吧帖子的html源文件，那么你就不要往下看了
        # 看了你也看不明白
        theradList = etree.HTML(raw)
        theradList = theradList.xpath(
            '//div[@class="p_postlist"]/div[@class="p_postlist"]/div[@class]')
        if theradList == []:
            Avalon.critical('程序无法正确获得文章内容')
            quit(1)
        finalList = []
        if self.debug:
            Avalon.debug_info('帖子内容获取成功')
        for perFloor in theradList:
            floorDict = {}
            # 更改了Xpath的匹配方式
            if self.debug:
                debugText = html.unescape(etree.tostring(perFloor).decode())
                debugText.replace('', '')
            if perFloor.xpath('./@data-field') == []:
                if self.debug:
                    Avalon.debug_info(
                        '因为不存在"data-field"属性,跳过对象"%s"' % str(perFloor))
                continue
            floorNum = json.loads(perFloor.xpath(
                './@data-field')[0])['content']['post_no']
            author = json.loads(perFloor.xpath(
                './@data-field')[0])['author']['user_name']
            text = perFloor.xpath('.//cc//div[@id]')[0]
            final_text = html.unescape(etree.tostring(text).decode())
            if self.debug:
                Avalon.debug_info('%s - %s' % (floorNum, author))
            floorDict['floor'] = int(floorNum)
            floorDict['author'] = author
            floorDict['text'] = final_text
            finalList.append(floorDict)
        #postFullInfo = self.postInfo()
        postFullInfo = self.postInfo
        postFullInfo['Data'] = finalList
        if useTemp is True:
            self.__tempSave.saveJson(postFullInfo, self.__workPageNumber)
        return(postFullInfo)


if __name__ == "__main__":
    Avalon.critical('模块非法调用!请运行Main.py!')
    quit(1)
