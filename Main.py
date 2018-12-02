#/usr/local/env python3
#__coding:utf-8 __
'''
百度贴吧下载器主程序

遵守GPL协议，侵权必究
'''
from Markdown import *
from Spider import *
from avalon_framework import *
import os

#现在写在这里的所有代码都只是临时解决方案
#会在短期内使用多线程解决
#所以没有注释（没有注释应该也能看懂）

while True:
    link = Avalon.gets('请输入帖子链接:\n[?]:')
    try:
        pid = int((link.split('/'))[-1].split('?')[0])
    except:
        Avalon.warning('输入错误！')
        pass
    else:
        pid = str(pid)
        Avalon.info('帖子ID:' + pid)
        break

see_lz = Avalon.ask('只看楼主？',True)

if see_lz:
    therad_link = 'https://tieba.baidu.com/p/%s?see_lz=1&pn=' % (pid)
    Avalon.info('Mode:Only Download Floor Owner')
else:
    therad_link = 'https://tieba.baidu.com/p/%s?pn=' % (pid)
    Avalon.info('Mode:Download all')

while True:
    filename = Avalon.gets('请输入要保存的文件名或目录+文件名，文件名必须以.md为后缀:\n[?]:')
    if filename.split('.')[-1] != 'md':
        Avalon.warning('文件名错误！')
        pass
    try:
        file = open(filename,'w+',1,'utf-8')
    except:
        Avalon.warning('文件错误！')
        pass
    else:
        break

Avalon.info('程序启动……')

for page_number in range(1,posts.page_num(posts.get(therad_link + '1')) + 1):
    Avalon.time_info('开始进行第%s页' % (str(page_number)))
    raw = posts.get(therad_link + str(page_number))
    for per_floor in posts.proccess(raw):
        file.write(Markdown.convert(per_floor))

file.close()