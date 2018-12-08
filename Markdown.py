#/usr/local/env python3
#__coding:utf-8 __
'''
Markdown转换模块（有奇怪的东西混进去了）

遵守GPL协议，侵权必究
'''

import html,json,re,time,os
from Image import image
from lxml import etree
from avalon_framework import Avalon

#正则表达式，用来匹配标签
_divTag = re.compile('<div[^>]*>')
_brTag = re.compile('<br\s*?/?>')

class markdown():

    def convert(resDict):
        #转换html到Markdown格式函数（按楼层转换）
        #如果你修改了在Spider.py中html的获取方式，此处逻辑需要修改
        authorInfo = str(resDict['floor']) + '楼|作者:' + resDict['author']
        lastInfo = '\n<div style="text-align:right;font-size:12px;color:#CCC;">%s</div>' % (authorInfo)
        resHTML = etree.HTML(resDict['text'])
        textHTML = resDict['text']
        #下面这一句是为了解决在正文开头莫名其妙出现空格的问题
        textHTML = textHTML.replace('            ','',1)
        #批量替换<a>标签（应该有更简单的解决办法）
        for a in resHTML.xpath('//a[@href]'):
            string = html.unescape(etree.tostring(a).decode())
            string = string.split('</a>',1)[0] + '</a>'
            if a.text != None:
                textHTML = textHTML.replace(string,a.text)
        #批量替换<img>标签
        for img in resHTML.xpath('//img[@class="BDE_Image"]'):
            string = html.unescape(etree.tostring(img).decode())
            imgBed = img.xpath('./@src')[0]
            #如果你需要使用图床，请取消下面一行的注释，但是这会大大减慢转换速度，同时带来部分Markdown解析的兼容性问题
            #imgBed = image.bedUpload(image.get(imgBed))
            link = '\n![%s](%s)' % (authorInfo,imgBed)
            textHTML = textHTML.replace(string,link)
        #替换其他标签
        textHTML = _divTag.sub('',textHTML)
        textHTML = textHTML.replace('</div>','')
        textHTML = _brTag.sub('\n',textHTML)
        
        return(textHTML + lastInfo + '\n\n---\n\n')