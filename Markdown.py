#/usr/local/env python3
#__coding:utf-8 __
'''
HTML to Markdown module.

followed GPL license
'''

import html,json,re,time,os,base64
from lxml import etree
from avalon_framework import Avalon
from Spider import posts
from urllib import parse
import urllib.request as url
import urllib.error as ure

div_tag = re.compile('<div[^>]*>')
br_tag = re.compile('<br\s*?/?>')

class Markdown():

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
                req = url.Request('https://image.mnixry.cn/public/api',postData)
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


    def convert(res_dict, compatible=True):
        if compatible:#The Feature may be comptible the markdown extra.
            pass
        else:
            pass
        
        author_info = str(res_dict['floor']) + '楼|作者:' + res_dict['author']
        last_info = '\n<div style="text-align:right;font-size:12px;color:#CCC;">%s</div>' % (author_info)
        res_html = etree.HTML(res_dict['text'])
        text_html = res_dict['text']

        text_html = text_html.replace('            ','',1)

        for a in res_html.xpath('//a[@href]'):
            string = html.unescape(etree.tostring(a).decode())
            string = string.split('</a>',1)[0] + '</a>'
            if a.text != None:
                text_html = text_html.replace(string,a.text)

        for img in res_html.xpath('//img[@class="BDE_Image"]'):
            string = html.unescape(etree.tostring(img).decode())
            imgBed = img.xpath('./@src')[0]
            #Remove comment of below line can enable Image bed mode,but the speed will be much slower
            #imgBed = Markdown.img_upload(img.xpath('./@src')[0])
            link = '\n![%s](%s)' % (author_info,imgBed)
            text_html = text_html.replace(string,link)

        text_html = div_tag.sub('',text_html)
        text_html = text_html.replace('</div>','')
        text_html = br_tag.sub('\n',text_html)
        text_html = final_markdown = text_html + last_info + '\n\n---\n\n'

        return(final_markdown)
        #<div style="text-align:right;font-size:12px;filter:alpha(Opacity=30);-moz-opacity:0.3;opacity: 0.3;">texthere</div>
        