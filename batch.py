from API import api
from avalon_framework import Avalon
import os


def singleBehavior(postID: int, savedFileName: str, seeLZ=True, imageBed=True):
    Avalon.debug_info('创建任务,ID:%d' % postID)
    if os.path.isfile(savedFileName):
        Avalon.time_info('帖子已经下载并保存,跳过[ID:%d]' % postID)
        return True
    post = api(postID=postID, seeLZ=seeLZ)
    try:
        postInfo = post.getInfo()
    except FileNotFoundError:
        return False
    except SystemExit:
        return False
    Avalon.time_info(
        '开始任务:"%s"(作者:%s)[ID:%d]' % (postInfo['Title'], postInfo['Author'],
                                     postID),
        highlight=True)
    Avalon.debug_info(postInfo)
    lastContext = []
    for i in range(1, postInfo['TotalPage'] + 1):
        Avalon.time_info('开始第%d页,共%d页' % (i, postInfo['TotalPage']))
        try:
            pageHTMLContent = post.getContent(i)
            pageMarkdownContent = post.contentToMarkdown(
                pageHTMLContent, useImageBed=imageBed)
        except KeyboardInterrupt:
            Avalon.critical('用户强制退出')
            quit(1)
        except SystemExit:
            pass
        else:
            lastContext.append(pageMarkdownContent)
    lastContext = ''.join(lastContext)
    post.saveToFile(savedFileName, lastContext)
    return True


filePath = Avalon.gets('请输入帖子目录文件路径:')
pathName = os.path.splitext(os.path.split(filePath)[-1])[0]
if not os.path.exists(pathName):
    os.mkdir(pathName)
with open(filePath) as f:
    perLink = f.readlines()
perID = []
for i in perLink:
    postID = int((i.split('/'))[-1].split('?')[0])
    perID.append(postID)
#Avalon.info(str(perID))
for i in perID:
    childFileName = str(i) + '.md'
    childPath = os.path.join(pathName, childFileName)
    # fullBehavior(postID=postID, fileName=fileName, onlySeeLZ=False)
    singleBehavior(postID=i, seeLZ=False, savedFileName=childPath)
