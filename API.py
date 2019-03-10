import threading
import json
import queue
import time
from Client import *
from Database import database
from avalon_framework import Avalon


class getThread():
    def __init__(self, postID: int):
        self.__db = database(pid=postID)
        self.__pageNumber = 1
        self.__tid = postID

    def __getMainThread(self, postID: int, pageNumber: int):
        context = getContext(threadID=postID, pageNumber=pageNumber)
        return context

    def __getSubFloor(self, postID: int, replyID: int, pageNumber: int):
        context = getReply(threadID=postID, replyID=replyID,
                           pageNumber=pageNumber)
        return context

    def multiThreadGetMain(self, threadNumber: int=8):
        workQueue = queue.Queue()
        threadLock = threading.Lock()
        exitFlag = False
        threadList = []

        def getBehavior(pageNumber: int):
            Avalon.debug_info('[%s]Thread Start Read Page %s' %
                              (self.__tid, pageNumber))
            if self.__db.checkExistPage(pageNumber):
                Avalon.debug_info(
                    '[%s]Page %s Had Already Exist in Database.' % (self.__tid, pageNumber))
                return
            result = self.__getMainThread(self.__tid, pageNumber)
            self.__db.writePage(pageNumber, result)

        def mainFloorThread():
            while not exitFlag:
                threadLock.acquire()
                if not workQueue.empty():
                    pageNumber = workQueue.get()
                    threadLock.release()
                    getBehavior(pageNumber)
                else:
                    threadLock.release()
                time.sleep(1)
        
        for i in range(threadNumber):
            newThread = threading.Thread(target=mainFloorThread)
            newThread.setName('PostThread #%s'%i)
            newThread.start()
            threadList.append(newThread)
        getBehavior(1)
        dbRead = self.__db.checkExistPage(1)[1]
        print(str(dbRead)[0:50])
        print(str(json.loads(dbRead)['page']))
        totalPages = json.loads(dbRead)['page']['total_page']
        totalPages = int(totalPages)
        for i in range(totalPages):
            workQueue.put(i+1)
        while not workQueue.empty():
            time.sleep(1)
        exitFlag = True
        for i in threadList:
            i.join(10)
        
        Avalon.info('Get All Pages Success')