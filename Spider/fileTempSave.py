from avalon_framework import Avalon
import os
import json
import re


class temp():
    def __init__(self, postID: int, workDir: str = os.getcwd(), tempDir: str = 'temp'):
        self.__fullTempDir = os.path.join(workDir, tempDir)
        self.__postID = int(postID)
        self.__fileNameMatch = re.compile(r'^TempSave_(\d+)_(\d+)\.(.+)$')
        if not os.path.exists(self.__fullTempDir):
            os.mkdir(self.__fullTempDir)

    def savePostRaw(self, postRaw: str, pageNumber: int, ext: str = 'html'):
        fullTempName = 'TempSave_%d_%d.%s' % (self.__postID, pageNumber, ext)
        fullTempFilePath = os.path.join(self.__fullTempDir, fullTempName)
        with open(fullTempFilePath, 'wt') as f:
            f.write(postRaw)
        return fullTempFilePath

    def saveJson(self, postInfo, pageNumber: int, ext: str = 'json'):
        fullTempName = 'TempSave_%d_%d.%s' % (self.__postID, pageNumber, ext)
        fullTempFilePath = os.path.join(self.__fullTempDir, fullTempName)
        with open(fullTempFilePath, 'wt') as f:
            postJson = json.dumps(postInfo)
            f.write(postJson)
        return fullTempFilePath

    def getSameTemp(self):
        sameTemp = {}
        dirList = os.listdir(self.__fullTempDir)
        for i in dirList:
            reResult = self.__fileNameMatch.split(i)
            while '' in reResult:
                reResult.remove('')
            if (len(reResult) == 3) and (int(reResult[0]) == self.__postID):
                if not sameTemp.get(reResult[2]):
                    sameTemp[reResult[2]] = []
                sameTemp[reResult[2]].append(tuple(reResult))
        return sameTemp

    def readFileByPath(self, fullPath: str):
        with open(fullPath, 'rt') as f:
            fileRes = f.read()
        return fileRes

    def readFileByID(self, infoTuple: tuple):
        fullFileName = 'TempSave_%s_%s.%s' % infoTuple
        fullFilePath = os.path.join(self.__fullTempDir, fullFileName)
        return self.readFileByPath(fullFilePath)
