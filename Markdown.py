#/usr/local/env python3
#__coding:utf-8 __
'''
HTML to Markdown module.
followed GPL license
'''

import html,json,re,time,os

class Markdown():

    def convert(html_res, compatible=True):
        if compatible:
            pass
        else:
            pass
        
        #<div style="text-align:right;font-size:12px;filter:alpha(Opacity=30);-moz-opacity:0.3;opacity: 0.3;">texthere</div>
        