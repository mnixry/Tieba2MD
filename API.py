from Markdown import markdown
from Image import image
from Spider import spider
from avalon_framework import Avalon
from lxml import etree
import os


class api():
    def __init__(self, postID: int, seeLZ: bool = True, debug: bool = False):
        self.__workSpider = spider(postID=postID, seeLZ=seeLZ, debug=debug)
        self.__workMarkdown = markdown()
        self.__workImage = image(debug=debug)

    def getInfo(self):
        return self.__workSpider.getPostInfo()

    def getContent(self, pageNumber: int):
        return self.__workSpider.getPost(pageNumber=pageNumber)

    def __imageBed(self, content: str):
        imageLinks = etree.HTML(content).xpath(
            '//img[@class="BDE_Image"]/@src')
        imageUploadedLinks = self.__workImage.uploadMultiImage(imageLinks)
        return imageUploadedLinks

    def contentToMarkdown(self, content: str, useImageBed: bool = True):
        markdownContent = []
        proccessdPost = self.__workSpider.proccessPost(content)
        if useImageBed is True:
            imageLinks = self.__imageBed(content=content)
        elif useImageBed is False:
            imageLinks = {}

        for i in proccessdPost['Data']:
            markdownContent.append(self.__workMarkdown.convert(
                resDict=i, imageBedLinksDict=imageLinks))

        return ''.join(markdownContent)

    def saveToFile(self, fileName: str, convedContent: str):
        with open(fileName, 'wt') as f:
            f.write(convedContent)
        return


"""
def fullBehavior(postID,fileName,onlySeeLZ=True):
    markdown = markdown()
    image = image(debug=GENERAL_DEBUG_MODE)
    posts = spider(postID=int(postID), seeLZ=onlySeeLZ)

    info = posts.getPostInfo()
    Avalon.info('帖子标题:%s,帖子作者:%s.' % (info['Title'], info['Author']))

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