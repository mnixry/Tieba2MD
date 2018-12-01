#/usr/local/env python3
#__coding:utf-8 __
'''
HTML to Markdown module.

followed GPL license
'''

import html,json,re,time,os
from lxml import etree

div_tag = re.compile('<div[^>]*>')
a_tag = re.compile('<a[^>]*>')
br_tag = re.compile('<br\s*?/?>')
img_tag = re.compile('')

class Markdown():

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

        for a in res_html.xpath('.//a[@href]'):
            string = html.unescape(etree.tostring(a).decode())
            string = string.split('</a>',1)[0] + '</a>'
            text_html = text_html.replace(string,a.text)

        for img in res_html.xpath('//img[@class="BDE_Image"]'):
            string = html.unescape(etree.tostring(img).decode())
            link = '\n![%s](%s)' % (author_info,img.xpath('./@src')[0])
            text_html = text_html.replace(string,link)

        text_html = div_tag.sub('',text_html)
        text_html = text_html.replace('</div>','')
        text_html = br_tag.sub('\n',text_html)
        text_html = final_markdown = text_html + last_info + '\n\n---\n\n'

        return(final_markdown)
        #<div style="text-align:right;font-size:12px;filter:alpha(Opacity=30);-moz-opacity:0.3;opacity: 0.3;">texthere</div>
        