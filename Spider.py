#/usr/local/env python3
#__coding:utf-8 __
'''
'''
from lxml import etree
from avalon_framework import Avalon
import urllib.request as url
import urllib.error as ure
import os,time,json,re,random,html

ua = open('user-agents.txt','rt',1,'utf-8','ignore')
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
        therad_list = etree.HTML((therad_read.read()).decode())
        therad_list = therad_list.xpath('//div[@class="l_post l_post_bright j_l_post clearfix  "]')
        for per_floor in therad_list:
            for i in per_floor.xpath('.//span[@class="tail-info"]/text()'):
                if i.find('楼') != -1:
                    floor = 'floor_' + str((i.replace('楼','')))
                else:
                    pass
                
            #floor = 'floor_' + str(((per_floor.xpath('.//span[@class="tail-info"]/text()'))[0]).replace('楼',''))
            author = (json.loads((per_floor.xpath('./@data-field'))[0]))['author']['user_name']
            text = (per_floor.xpath('.//div[@class="d_post_content j_d_post_content "]'))[0]
            final_text = html.unescape(etree.tostring(text).decode())
            print(floor,author,final_text)

therad.get('http://dq.tieba.com/p/3363856719?pn=1')#test line