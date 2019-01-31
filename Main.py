#/usr/local/env python3
#__coding:utf-8 __
#Project Link:https://github.com/mnixry/Tieba2MD
'''
百度贴吧下载器主程序

遵守GPL协议，侵权必究
'''

from Markdown import markdown
from Spider import spider
from avalon_framework import Avalon
from Image import image
from Image import fileUpload
from lxml import etree
import os

USE_IMAGE_BED = True
GENERAL_DEBUG_MODE = False

while True:
    link = Avalon.gets('请输入帖子链接:')
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
    fileName = Avalon.gets('请输入要保存的文件名，必须以.md为后缀:')
    if fileName.split('.')[-1] != 'md':
        Avalon.warning('文件名错误！')
    else:
        try:
            file = open(fileName, 'w+', 1, 'utf-8')
        except:
            Avalon.warning('文件错误!')
        else:
            break

posts = spider(debug=GENERAL_DEBUG_MODE)
markdown = markdown()
image = image(debug=GENERAL_DEBUG_MODE)

Avalon.info('程序启动……', highlight=True)

for pageNumber in range(1, posts.pageNumber(posts.getPost(postLink + '1')) + 1):
    Avalon.time_info('开始进行第%s页' % (str(pageNumber)))
    raw = posts.getPost(postLink + str(pageNumber))
    gotImg = etree.HTML(raw).xpath('//img[@class="BDE_Image"]/@src')
    if USE_IMAGE_BED:
        imgLink = image.uploadMultiImage(gotImg)
    else:
        imgLink = {}
        for i in gotImg:
            imgLink[i] = str(i)
    for perFloor in posts.proccessPost(raw):
        file.write(markdown.convert(perFloor, imgLink))

del posts, markdown, image
file.flush().close()
