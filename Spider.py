#/usr/local/env python3
#__coding:utf-8 __
'''
百度贴吧帖子下载/处理模块
版本：1.4

遵守GPL协议，侵权必究
'''
from lxml import etree
from avalon_framework import Avalon
from urllib import request,error
import os,time,json,random,html

#User-Agent获取，请确保“user-agents.txt”存在！
_userAgent = (open('user-agents.txt','rt',1,'utf-8','ignore')).readlines()

class posts():
    
    def getPost(link):#获得html源文件函数
        while True:#这是一个死循环，直到程序正常获得数据才结束
            try:
                postRequest = request.Request(link)
                try:
                    #设置程序请求头，伪装爬虫（必要性存疑）
                    postRequest.add_header('User-Agent',(random.choice(_userAgent)).replace('\n',''))
                    postRequest.add_header('Referer','https://tieba.baidu.com')
                except:
                    pass
                else:
                    postRead = request.urlopen(postRequest).read()
            #错误处理
            except error.URLError as e:
                Avalon.warning("访问失败!原因:%s" % (str(e)))
            except KeyboardInterrupt:
                Avalon.error("用户强制退出")
                quit()
            except:
                Avalon.warning("出现未知错误!")
            #没有错误，结束循环
            else:
                break
        return(postRead.decode())

    def pageNumber(raw):#从html源文件中选取总计页数
        floorGet = etree.HTML(raw)
        floorXpath = floorGet.xpath('//div[@class="pb_footer"]//li[@class="l_reply_num"]//input/@max-page')
        if floorXpath != []:
            return(int(floorXpath[0]))
        else:
            return(0)

    def proccessPost(raw):#将源文件转换为dict类型的数据
        #如果你没有读过百度贴吧帖子的html源文件，那么你就不要往下看了
        #看了你也看不明白
        theradList = etree.HTML(raw)
        theradList = theradList.xpath('//div[@class="l_post j_l_post l_post_bright  "]')
        finalList = []
        for perFloor in theradList:
            floorDict = {}
            #没问题了 
            #不知为何，百度贴吧修改了代码
            #如果在此版本放出后一个月内百度贴吧代码再次修改
            #我会考虑将此项目闭源或者通过css分析元素(不会做,除非找到人帮我做,不然我只能选择闭源)
            floorNum = json.loads(perFloor.xpath('./@data-field')[0])['content']['post_no']
            author = json.loads(perFloor.xpath('./@data-field')[0])['author']['user_name']
            text = perFloor.xpath('.//div[@class="d_post_content j_d_post_content  clearfix"]')[0]
            final_text = html.unescape(etree.tostring(text).decode())
            floorDict['floor'] = int(floorNum)
            floorDict['author'] = author
            floorDict['text'] = final_text
            finalList.append(floorDict)
        return(finalList)