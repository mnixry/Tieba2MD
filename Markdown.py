#/usr/local/env python3
#__coding:utf-8 __
'''
Markdown转换模块（有奇怪的东西混进去了）

遵守GPL协议，侵权必究
'''

import html,json,re,time,os,base64
from lxml import etree
from avalon_framework import Avalon
from Spider import posts
from urllib import parse
import urllib.request as url
import urllib.error as ure

#正则表达式，用来匹配标签
div_tag = re.compile('<div[^>]*>')
br_tag = re.compile('<br\s*?/?>')

class Markdown():
    #图床上传函数（暂时没有使用，如果需要使用请自行取消在convert函数中的注释）
    def img_upload(org_link):
        postData = {}
        postData['key'] = 2333
        postData['OnlyUrl'] = 0
        img = posts.get_image(org_link)
        img_encoded = base64.b64encode(img)
        postData['imgBase64'] = img_encoded
        postData = parse.urlencode(postData).encode()
        while True:
            try:
                req = url.Request('https://image.mnixry.cn/public/api',postData)#image.mnixry.cn是我本人的图床站点，如果不可用请从业务逻辑上去除这些部分
                req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36')
                json_back = url.urlopen(req)
            except ure.URLError as e:
                Avalon.warning('Error:' + str(e))
            else:
                ref_dict = json.loads(json_back.read().decode())
                if ref_dict['code'] == '1':
                    break
        ref_link = ref_dict['img']
        return(ref_link)


    def convert(res_dict):
        #转换html到Markdown格式函数（按楼层转换）
        #如果你修改了在Spider.py中html的获取方式，此处逻辑需要修改
        author_info = str(res_dict['floor']) + '楼|作者:' + res_dict['author']
        last_info = '\n<div style="text-align:right;font-size:12px;color:#CCC;">%s</div>' % (author_info)
        res_html = etree.HTML(res_dict['text'])
        text_html = res_dict['text']
        #下面这一句是为了解决在正文开头莫名其妙出现空格的问题
        text_html = text_html.replace('            ','',1)

        #批量替换<a>标签（应该有更简单的解决办法）
        for a in res_html.xpath('//a[@href]'):
            string = html.unescape(etree.tostring(a).decode())
            string = string.split('</a>',1)[0] + '</a>'
            if a.text != None:
                text_html = text_html.replace(string,a.text)
        #批量替换<img>标签
        for img in res_html.xpath('//img[@class="BDE_Image"]'):
            string = html.unescape(etree.tostring(img).decode())
            imgBed = img.xpath('./@src')[0]
            #如果你需要使用图床，请取消下面一行的注释，但是这会大大减慢转换速度，同时带来部分Markdown解析的兼容性问题
            #imgBed = Markdown.img_upload(img.xpath('./@src')[0])
            link = '\n![%s](%s)' % (author_info,imgBed)
            text_html = text_html.replace(string,link)
        #替换其他标签
        text_html = div_tag.sub('',text_html)
        text_html = text_html.replace('</div>','')
        text_html = br_tag.sub('\n',text_html)
        text_html = final_markdown = text_html + last_info + '\n\n---\n\n'

        return(final_markdown)
        