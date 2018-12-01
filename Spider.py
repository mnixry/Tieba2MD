#/usr/local/env python3
#__coding:utf-8 __
'''
Baidu Tieba download module.
Version:1.1
Last Edit:2018.12.01

fllowed GPL license.
'''
from lxml import etree
from avalon_framework import Avalon
import urllib.request as url
import urllib.error as ure
import os,time,json,random,html

ua = open('user-agents.txt','rt',1,'utf-8','ignore')#user agents get(Please make sure user-agents.txt exist!)
user_agent = ua.readlines()

class therad():
    
    def get(link):
        while True:#The long while untill the resource got
            try:
                therad = url.Request(link)
                try:
                    #Set the Headers to hide the spider(UAs from @sqlmap)
                    therad.add_header('User-Agent',(random.choice(user_agent)).replace('\n',''))
                    therad.add_header('Referer','https://tieba.baidu.com')
                except:
                    pass
                else:
                    therad_read = url.urlopen(therad)
            except ure as status:
                Avalon.warning("Access Tieba Error!Please Check the link you input!Error Reason:\n%s" % (str(status)))
                pass
            except:
                print("Unkonwn Error!")
                pass
            else:
                break
        return(therad_read.read().decode())

    def get_image(link):
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

    def page_num(raw):
        floor_get = etree.HTML(raw)
        floor_xpath = floor_get.xpath('//div[@class="pb_footer"]//li[@class="l_reply_num"]//input/@max-page')
        return(int(floor_xpath[0]))

    def proccess(raw):
        therad_list = etree.HTML(raw)
        therad_list = therad_list.xpath('//div[@class="l_post l_post_bright j_l_post clearfix  "]')
        final_list = []
        for per_floor in therad_list:
            floor_dict = {}
            for i in per_floor.xpath('.//span[@class="tail-info"]/text()'):
                if i.find('楼') != -1:
                    floor = int((i.replace('楼','')))
                else:
                    pass
            
            #floor = 'floor_' + str(((per_floor.xpath('.//span[@class="tail-info"]/text()'))[0]).replace('楼',''))
            author = (json.loads((per_floor.xpath('./@data-field'))[0]))['author']['user_name']
            text = (per_floor.xpath('.//div[@class="d_post_content j_d_post_content "]'))[0]
            final_text = html.unescape(etree.tostring(text).decode())
            floor_dict['floor'] = floor
            floor_dict['author'] = author
            floor_dict['text'] = final_text
            final_list.append(floor_dict)
        return(final_list)

#print(therad.proccess(therad.get('http://dq.tieba.com/p/3363856719?pn=1')))#test line
#therad.floor_num(therad.get('http://dq.tieba.com/p/3363856719?pn=1'))