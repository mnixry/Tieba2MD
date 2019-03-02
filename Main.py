#/usr/local/env python3
#__coding:utf-8 __
#Project Link:https://github.com/mnixry/Tieba2MD
'''
百度贴吧下载器主程序

遵守GPL协议，侵权必究
'''

from API import api
from avalon_framework import Avalon
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

while True:
    fileName = Avalon.gets('请输入要保存的文件名，必须以.md为后缀:')
    if fileName.split('.')[-1] != 'md':
        Avalon.warning('文件名错误！')
    else:
        try:
            with open(fileName, 'w+', encoding='utf-8') as f:
                if not f.writable:
                    raise Exception
        except:
            Avalon.warning('文件错误!')
        else:
            break

Avalon.debug_info('程序已经启动...正在获取帖子信息')
post = api(postID=postID, seeLZ=onlySeeLZ, debug=GENERAL_DEBUG_MODE)
postInfo = post.getInfo()
Avalon.time_info('开始任务:"%s"(作者:%s)' %
                 (postInfo['Title'], postInfo['Author']), highlight=True)
for i in range(1, postInfo['TotalPage']):
    Avalon.time_info('开始第%d页,共%d页' % (i, postInfo['TotalPage']))
    try:
        pageHTMLContent = post.getContent(i)
        pageMarkdownContent = post.contentToMarkdown(
            pageHTMLContent, useImageBed=USE_IMAGE_BED)
    except KeyboardInterrupt:
        Avalon.critical('用户强制退出')
        quit(1)
    else:
        post.saveToFile(fileName, pageMarkdownContent)


"""
markdown = markdown()
image = image(debug=GENERAL_DEBUG_MODE)

fullBehavior(postID=postID,fileName=fileName,onlySeeLZ=onlySeeLZ)

def fullBehavior(postID,fileName,onlySeeLZ=True):
    posts = spider(postID=int(postID), seeLZ=onlySeeLZ)

    info = posts.getPostInfo()
    Avalon.info('帖子标题:%s,帖子作者%s.' % (info['title'], info['author']))

    Avalon.info('程序启动……', highlight=True)

    totalPageNumber = int(posts.getPostInfo()['TotalPage'])
    finalMarkdown = ''
    try:
        for pageNumber in range(1, totalPageNumber + 1):
            Avalon.time_info('[%d]开始进行第%d页,共%d页' %
                            (postID, pageNumber, totalPageNumber))
            raw = posts.getPost(int(pageNumber))
            gotImg = etree.HTML(raw).xpath('//img[@class="BDE_Image"]/@src')
            if USE_IMAGE_BED:
                imgLink = image.uploadMultiImage(gotImg)
            else:
                imgLink = {}
                for i in gotImg:
                    imgLink[i] = str(i)
            for perFloor in posts.proccessPost(raw):
                finalMarkdown = finalMarkdown + markdown.convert(perFloor, imgLink)
    except KeyboardInterrupt:
        Avalon.critical('用户强制退出')
    finally:
        del posts, markdown, image
        with open(fileName, 'w+', encoding='utf-8') as f:
            f.write(finalMarkdown)
"""
