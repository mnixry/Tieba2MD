#/usr/local/env python3
#__coding:utf-8 __
'''
百度贴吧下载器主程序

遵守GPL协议，侵权必究
'''

from Markdown import markdown
from Spider import spider
from avalon_framework import Avalon
from Image import image
from lxml import etree
import os

#现在写在这里的所有代码都只是临时解决方案
#会在短期内使用多线程解决
#所以没有注释（没有注释应该也能看懂）


imageBed = False

while True:
    link = Avalon.gets('请输入帖子链接:\n[?]:')
    try:
        postID = int((link.split('/'))[-1].split('?')[0])
    except:
        Avalon.warning('输入错误！')
        pass
    else:
        postID = str(postID)
        Avalon.info('帖子ID:' + postID)
        break

onlySeeLZ = Avalon.ask('只看楼主？', True)

if onlySeeLZ:
    postLink = 'https://tieba.baidu.com/p/%s?see_lz=1&ajax=1&pn=' % (postID)
    Avalon.info('模式:只看楼主', highlight=True)
else:
    postLink = 'https://tieba.baidu.com/p/%s?ajax=1&pn=' % (postID)
    Avalon.info('模式:全部', highlight=True)

while True:
    fileName = Avalon.gets('请输入要保存的文件名或目录+文件名，文件名必须以.md为后缀:\n[?]:')
    if fileName.split('.')[-1] != 'md':
        Avalon.warning('文件名错误！')
    else:
        try:
            file = open(fileName, 'w+', 1, 'utf-8')
        except:
            Avalon.warning('文件错误!')
        else:
            break

posts = spider(debug=True)
markdown = markdown()
image = image(debug=False)

Avalon.info('程序启动……', highlight=True)

for pageNumber in range(1, posts.pageNumber(posts.getPost(postLink + '1')) + 1):
    Avalon.time_info('开始进行第%s页' % (str(pageNumber)))
    raw = posts.getPost(postLink + str(pageNumber))
    gotImg = etree.HTML(raw).xpath('//img[@class="BDE_Image"]/@src')
    if imageBed:
        #print(gotImg)
        imgLink = image.multiThread(gotImg)
    else:
        imgLink = {}
        for i in gotImg:
            imgLink[i] = str(i)
    for perFloor in posts.proccessPost(raw):
        file.write(markdown.convert(perFloor,imgLink))

file.close()
