from API import api
from avalon_framework import Avalon
import os

def singleBehavior(postID:int,savedFileName:str,seeLZ=True,imageBed=True):
    post = api(postID=postID, seeLZ=seeLZ)
    postInfo = post.getInfo()
    Avalon.time_info('开始任务:"%s"(作者:%s)' %
                    (postInfo['Title'], postInfo['Author']), highlight=True)
    Avalon.debug_info(postInfo)
    for i in range(1, postInfo['TotalPage']+1):
        Avalon.time_info('开始第%d页,共%d页' % (i, postInfo['TotalPage']))
        try:
            pageHTMLContent = post.getContent(i)
            pageMarkdownContent = post.contentToMarkdown(
                pageHTMLContent, useImageBed=imageBed)
        except KeyboardInterrupt:
            Avalon.critical('用户强制退出')
            quit(1)
        else:
            post.saveToFile(savedFileName, pageMarkdownContent)

filePath = Avalon.gets('请输入帖子目录文件路径:')
with open(filePath) as f:
    perLink = f.readlines()
perID = []
for i in perLink:
    postID = int((i.split('/'))[-1].split('?')[0])
    perID.append(postID)
#Avalon.info(str(perID))
for i in perID:
    fileName = str(postID) + '.md'
    # fullBehavior(postID=postID, fileName=fileName, onlySeeLZ=False)
    singleBehavior(postID=i,seeLZ=False,savedFileName=fileName)