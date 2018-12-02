#/usr/local/env python3
#__coding:utf-8 __
'''
百度贴吧帖子下载/处理模块
版本：1.4

遵守GPL协议，侵权必究
'''
from lxml import etree
from avalon_framework import Avalon
import urllib.request as url
import urllib.error as ure
import os,time,json,random,html

#User-Agent获取，请确保“user-agents.txt”存在！
ua = open('user-agents.txt','rt',1,'utf-8','ignore')
user_agent = ua.readlines()

class posts():
    
    def get(link):#获得html源文件函数
        while True:#这是一个死循环，直到程序正常获得数据才结束
            try:
                therad = url.Request(link)
                try:
                    #设置程序请求头，伪装爬虫（必要性存疑）
                    therad.add_header('User-Agent',(random.choice(user_agent)).replace('\n',''))
                    therad.add_header('Referer','https://tieba.baidu.com')
                except:
                    pass
                else:
                    therad_read = url.urlopen(therad)
            #错误处理
            except ure.URLError as status:
                Avalon.warning("Access Tieba Error!Please Check the link you input!Error Reason:\n%s" % (str(status.reason)))
            except ure.HTTPError as status:
                Avalon.warning("Access Tieba Error!Please Check the link you input!Error Reason:\n%s" % (str(status.reason)))
            except:
                Avalon.warning("Unknown Error!")
            #没有错误，结束循环
            else:
                break
        return(therad_read.read().decode())

    def get_image(link):#图片下载函数，逻辑同get函数
        while True:
            try:
                image = url.Request(link)
                image.add_header('User-Agent',(random.choice(user_agent)).replace('\n',''))
                image.add_header('Referer','https://tieba.baidu.com')
                image_read = url.urlopen(image)
            except:
                pass
            else:
                return(image_read.read())

    def page_num(raw):#从html源文件中选取总计页数
        floor_get = etree.HTML(raw)
        floor_xpath = floor_get.xpath('//div[@class="pb_footer"]//li[@class="l_reply_num"]//input/@max-page')
        if floor_xpath != []:
            return(int(floor_xpath[0]))
        else:
            return(0)

    def proccess(raw):#将源文件转换为dict类型的数据
        #如果你没有读过百度贴吧帖子的html源文件，那么你就不要往下看了
        #看了你也看不明白
        therad_list = etree.HTML(raw)
        therad_list = therad_list.xpath('//div[@class="l_post l_post_bright j_l_post clearfix  "]')
        final_list = []
        for per_floor in therad_list:
            floor_dict = {}
            for i in per_floor.xpath('.//span[@class="tail-info"]/text()'):
                if i.find('楼') != -1:
                    floor = int((i.replace('楼','')))
            #在这里我发现一个非常严重的问题
            #其实我们需要获取的所有数据都以json格式存在于“data-field”属性中
            #而我在这里明显把它搞复杂了
            #因为此代码现在还能够工作，而且效率预计相差不大
            #所以不准备对这里进行修改（其实是懒）
            #如果有能改的人，欢迎Pull request
            author = (json.loads((per_floor.xpath('./@data-field'))[0]))['author']['user_name']
            text = (per_floor.xpath('.//div[@class="d_post_content j_d_post_content "]'))[0]
            final_text = html.unescape(etree.tostring(text).decode())
            floor_dict['floor'] = floor
            floor_dict['author'] = author
            floor_dict['text'] = final_text
            final_list.append(floor_dict)
        return(final_list)