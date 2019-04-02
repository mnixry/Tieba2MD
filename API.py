import threading
import json
import queue
import time
from Client import getReply, formatJson, getContext, getUser
from avalon_framework import Avalon
from Database import database
from math import ceil


class getThread():
    def __init__(self, postID: int):
        self.__db = database(pid=postID)
        self.__tid = postID
        self.__executeCommand = self.__db.executeCommand()
        self.__dbTotalChange = 0

        def autoWrite():
            for i in self.__executeCommand:
                self.__dbTotalChange = int(i)

        self.autoWriteThread = threading.Thread(target=autoWrite)
        self.autoWriteThread.start()

    @staticmethod
    def __getMainThread(postID: int, pageNumber: int):
        context = getContext(threadID=postID, pageNumber=pageNumber)
        return context

    @staticmethod
    def __getSubFloor(postID: int, replyID: int, pageNumber: int):
        context = getReply(
            threadID=postID, replyID=replyID, pageNumber=pageNumber)
        return context

    @staticmethod
    def __calcPageNum(PageSize: int, TotalNum: int):
        if PageSize == 0:
            return 0
        PageNumber = ceil(TotalNum / PageSize)
        return int(PageNumber)

    def __getPostBehavior(self, pageNumber: int, threadName: str):
        Avalon.debug_info('[%s]Thread "%s" Start Read Page %s' %
                          (self.__tid, threadName, pageNumber))
        if self.__db.checkExistPage(pageNumber):
            Avalon.debug_info('[%s]Page %s Had Already Exist in Database.' %
                              (self.__tid, pageNumber))
            return
        result = self.__getMainThread(self.__tid, pageNumber)
        self.__db.writePage(pageNumber, result)
        return self.__dbTotalChange

    def __getSubPageBehavior(self, replyID: int, replyPageNumber: int,
                             threadName: str):
        Avalon.debug_info('[%s]Thread "%s" Start Read Reply %s - Page %s' %
                          (self.__tid, threadName, replyID, replyPageNumber))
        if self.__db.checkExistSubPage(replyID, replyPageNumber):
            Avalon.debug_info(
                '[%s]Reply %s - Page %s Had Already Exist in Database.' %
                (self.__tid, replyID, replyPageNumber))
            return
        result = self.__getSubFloor(self.__tid, replyID, replyPageNumber)
        self.__db.writeSubPage(replyID, replyPageNumber, result)
        return self.__dbTotalChange

    def __writePageUserNameToDatabase(self, gotData: dict):
        for i in gotData['user_list']:
            userID = int(i['id'])
            userName = str(i.get('name', ''))
            if not userName:
                userName = str(i.get('name_show', ''))
                if not userName:
                    userName = str(userID)
            userData = json.dumps(i)
            self.__db.writeUsers(userID, userName, userData)

    def __getUserName(self, userID: str):
        dbResult = self.__db.checkExistUsers(userID)
        if not dbResult:
            Avalon.debug('User ID: %s Can\'t Get Username,Will Use ID Instead.'
                         % userID)
            userName = str(userID)
        else:
            userName = str(dbResult[1])
        return userName

    def __getReplyIDList(self, pageNumber: int):
        dbResult = self.__db.checkExistPage(pageNumber)
        if not dbResult:
            Avalon.error('Failed To Get Page %s In Database' % pageNumber)
            return False
        dbResultDecode = json.loads(dbResult)
        replyIDList = []
        for perFloor in dbResultDecode['post_list']:
            replyID = perFloor.get('id')
            if replyID:
                replyIDList.append(int(replyID))
        return replyIDList

    def multiThreadGetMain(self, threadNumber: int = 8):
        workQueue = queue.Queue(threadNumber)
        threadLock = threading.Lock()
        exitFlag = False
        threadList = []

        def mainFloorThread(name: str = 'Untitled'):
            while not exitFlag:
                threadLock.acquire()
                if not workQueue.empty():
                    pageNumber = workQueue.get()
                    threadLock.release()
                    self.__getPostBehavior(pageNumber, name)
                else:
                    threadLock.release()
                    time.sleep(1)

        for i in range(threadNumber):
            threadName = 'PostThread #%s' % i
            newThread = threading.Thread(
                target=mainFloorThread, args=(threadName, ))
            newThread.setName(threadName)
            newThread.start()
            threadList.append(newThread)

        self.__getPostBehavior(1, threadName='PreSetThread')
        dbRead = self.__db.checkExistPage(1)[1]
        if not dbRead:
            Avalon.critical('Can\'t Get Page 1,Program Exit!')
            quit(1)
        totalPages = int(json.loads(dbRead)['page']['total_page'])
        for i in range(totalPages):
            workQueue.put(i + 1)
        while not workQueue.empty():
            time.sleep(1)
        exitFlag = True
        for i in threadList:
            i.join()
        Avalon.info('[%s]Get All Pages Success' % self.__tid)

    def convDataToPerFloor(self):
        dbGot = json.loads(self.__db.checkExistPage(1)[1])
        totalPage = int(dbGot['page']['total_page'])

        for pageNum in range(totalPage):
            gotData = self.__db.checkExistPage(pageNum + 1)
            if not gotData:
                Avalon.error('Can\'t Get Page %s,Skip' % pageNum)
                continue

            gotData = json.loads(gotData[1])
            self.__writePageUserNameToDatabase(gotData)
            for i in gotData['post_list']:
                replyID = int(i['id'])
                replyNum = int(i.get('sub_post_number', 0))
                floorNumber = int(i['floor'])
                publishTime = int(i['time'])
                userID = int(i['author_id'])
                userName = self.__getUserName(userID)
                context = str(json.dumps(i))
                self.__db.writeFloor(floorNumber, replyID, replyNum,
                                     publishTime, userName, context)

            Avalon.debug_info(
                '[%s]Floor Info at Page %s Finished.Database Changed %s Record'
                % (self.__tid, pageNum + 1, self.__dbTotalChange))

    def multiThreadGetSubPage(self,
                              threadNumber: int = 16,
                              expectedPageSize: int = 30):
        workQueue = queue.Queue(threadNumber)
        threadLock = threading.Lock()
        exitFlag = False
        threadList = []

        def subPageThread(name: str = 'Untitled'):
            while not exitFlag:
                threadLock.acquire()
                if not workQueue.empty():
                    getArgs = workQueue.get()
                    threadLock.acquire()
                    self.__getSubPageBehavior(*getArgs, name)
                else:
                    threadLock.release()
                    time.sleep(1)

        for i in range(threadNumber):
            threadName = 'SubFloorThread#%s' % i
            newThread = threading.Thread(
                target=subPageThread, args=(threadName, ))
            newThread.setName(threadName)
            newThread.start()
            threadList.append(newThread)

        totalFloorNumber = self.__db.getlastFloorNum()
        print(totalFloorNumber)
        for floorNum in range(totalFloorNumber):
            dbResult = self.__db.checkExistFloor(floorNum + 1)
            if not dbResult:
                continue
            replyID = dbResult[1]
            replyNumber = dbResult[2]
            replyPageNumber = self.__calcPageNum(expectedPageSize, replyNumber)
            for i in range(replyPageNumber):
                workQueue.put((replyID, i + 1))
        while not workQueue.empty():
            time.sleep(1)
        exitFlag = 1
        for i in threadList:
            i.join()
        Avalon.info('[%s] Get Sub Floor Page Success' % self.__tid)
