#/usr/local/env python3
#__coding:utf-8 __
#Project Link:https://github.com/mnixry/Tieba2MD
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
import os
import time
import json
import random
import html


def executeTime(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        startTime = time.time()*1000
        result = func(*args, **kwargs)
        if True:
            totalTime = time.time()*1000 - startTime
            totalTime
        return(result)
    return(wrapper)


class spider():
    def __init__(self:None, debug:bool=False):
        #User-Agent获取，请确保“user-agents.txt”存在
        with open('user-agents.txt', 'rt',errors='ignore') as fileRead:
            self.__userAgent = fileRead.readlines()
        Avalon.info('模块Spider.py已加载')
        if debug:
            self.debug = True
        elif not debug:
            self.debug = False
        else:
            raise TypeError

    @executeTime
    def getPost(self:None, link:str):  # 获得html源文件函数
        for tryTimes in range(1, 11):  # 这是一个死循环，直到程序正常获得数据才结束
            try:
                postRequest = request.Request(link)
                try:
                    #设置程序请求头，伪装爬虫（必要性存疑）
                    postRequest.add_header(
                        'User-Agent', (random.choice(self.__userAgent)).replace('\n', ''))
                    postRequest.add_header(
                        'Referer', 'https://tieba.baidu.com')
                except:
                    continue
                else:
                    postRead = request.urlopen(postRequest, timeout=4).read()
                    if self.debug:
                        Avalon.debug_info('Link %s, Header Finished.' % link)
            #错误处理
            except error.URLError as e:
                Avalon.warning("访问失败!原因:%s(%s/10)" %
                               (str(e.reason), str(tryTimes)))
            except timeout as e:
                Avalon.warning("访问失败!原因:%s(%s/10)" % (str(e), str(tryTimes)))
            except KeyboardInterrupt:
                Avalon.critical("用户强制退出")
                quit(1)
            except:
                Avalon.warning("出现未知错误!(%s/10)" % tryTimes)
            #没有错误，结束循环
            else:
                if self.debug:
                    Avalon.debug_info('Link %s Get Successed.' % link)
                break
        else:
            Avalon.error('获取失败!')
            if self.debug:
                Avalon.debug('Link:%s' % link)
        return(postRead.decode())

    @executeTime
    def pageNumber(self:None, raw:str):  # 从html源文件中选取总计页数
        floorGet = etree.HTML(raw)
        floorXpath = floorGet.xpath(
            '//div/div[@id="ajax-down"]//div[@id]//li/span[@class="red"][last()]/text()')
        if floorXpath != []:
            return(int(floorXpath[0]))
        else:
            Avalon.critical('程序无法正确获得帖子页数')
            quit(1)

    @executeTime
    def proccessPost(self:None, raw:str):  # 将源文件转换为dict类型的数据
        #如果你没有读过百度贴吧帖子的html源文件，那么你就不要往下看了
        #看了你也看不明白
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
            #更改了Xpath的匹配方式
            if self.debug:
                debugText = html.unescape(etree.tostring(perFloor).decode())
                debugText.replace('', '')
            if perFloor.xpath('./@data-field') == []:
                if self.debug:
                    Avalon.debug_info('因为不存在 "data-field",跳过对象 "%s"'%str(perFloor))
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
        return(finalList)


if __name__ == "__main__":
    Avalon.critical('模块非法调用!请运行Main.py!')
    quit(1)
