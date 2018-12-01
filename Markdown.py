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

        html_res = div_tag.sub('',res_dict['text'])
        html_res = '<a></a>' + html_res
        html_res = html_res.replace('</div>','')
        html_res = br_tag.sub('\n',html_res)
        html_res = a_tag.sub('',html_res)
        html_res = html_res.replace('</a>','')
        last_info = str(res_dict['floor']) + '楼|作者:' + res_dict['author']
        html_res = html_res + '\n<div style="text-align:right;font-size:12px;color:#CCC;">%s</div>' % (last_info)
        final_markdown = html_res + '\n\n---\n\n'

        return(final_markdown)
        #<div style="text-align:right;font-size:12px;filter:alpha(Opacity=30);-moz-opacity:0.3;opacity: 0.3;">texthere</div>
        