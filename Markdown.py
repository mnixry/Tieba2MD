#/usr/local/env python3
#__coding:utf-8 __
'''
HTML to Markdown module.
followed GPL license
'''

import html,json,re,time,os
from lxml import etree

div_tag = re.compile('<\s*div[^>]*>[^<]*')
a_tag = re.compile('<\s*a[^>]*>[^<]*')
br_tag = re.compile('<br\s*?/?>')
img_tag = re.compile('')

class Markdown():

    def convert(html_res, compatible=True):
        if compatible:
            pass
        else:
            pass

        html_res = div_tag.sub('',html_res)
        html_res = html_res.replace('</div>','',1)
        html_res = br_tag.sub('\n',html_res)
        html_res = a_tag.sub('',html_res)
        html_res = html_res.replace('</a>','')
        
        #<div style="text-align:right;font-size:12px;filter:alpha(Opacity=30);-moz-opacity:0.3;opacity: 0.3;">texthere</div>
        