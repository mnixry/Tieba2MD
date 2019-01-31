#/usr/local/env python3
#__coding:utf-8 __
'''
Markdown转换模块

遵守GPL协议，侵权必究
'''

import html
import json
import re
import time
import os
from Image import image
from lxml import etree
from avalon_framework import Avalon

#正则表达式，用来匹配标签
_divTag = re.compile(r'<div[^>]*>')
_brTag = re.compile(r'<br\s*?/?>')


class markdown():
    def __init__(self: None):
        #Avalon.info('模块Markdown.py已加载')
        pass

    def convert(self: None, resDict: dict, imageBedLinksDict: dict, wrap: int = 1):
        #这里新增了一个wrap参数用于指定换行符个数
        if type(wrap) != int:
            raise TypeError
        elif wrap > 2:
            wrap = 2
        elif wrap < 0:
            wrap = 1
        #转换html到Markdown格式函数（按楼层转换）
        authorInfo = str(resDict['floor']) + '楼|作者:' + resDict['author']
        lastInfo = '\n<div style="text-align:right;font-size:12px;color:#CCC;">%s</div>' % (
            authorInfo)
        resHTML = etree.HTML(resDict['text'])
        textHTML = resDict['text']
        #下面这一句是为了解决在正文开头莫名其妙出现空格的问题
        textHTML = textHTML.replace('            ', '', 1)
        #批量替换<a>标签（应该有更简单的解决办法）
        for a in resHTML.xpath('//a[@href]'):
            string = html.unescape(etree.tostring(a).decode())
            string = string.split('</a>', 1)[0] + '</a>'
            if a.text != None:
                textHTML = textHTML.replace(string, a.text)
        #批量替换<img>标签
        for img in resHTML.xpath('//img[@class="BDE_Image"]'):
            string = html.unescape(etree.tostring(img).decode())
            imgBedOriginLink = img.xpath('./@src')[0]
            imgBedLink = imageBedLinksDict[imgBedOriginLink]
            if imgBedLink == imgBedOriginLink:
                authorInfo = authorInfo + '|【使用原图】'
            link = '\n![%s](%s)\n' % (authorInfo, imgBedLink)
            textHTML = textHTML.replace(string, link)
        #替换其他标签
        textHTML = _divTag.sub('', textHTML)
        textHTML = textHTML.replace('</div>', '')
        textHTML = _brTag.sub('\n'*wrap, textHTML)

        return(textHTML + lastInfo + '\n\n---\n\n')


if __name__ == "__main__":
    Avalon.critical('模块非法调用!请运行Main.py!')
    quit()
