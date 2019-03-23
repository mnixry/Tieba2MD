import sqlite3
import json
import threading
from time import sleep
from queue import Queue


class database():
    def __init__(self, pid: int):
        fileName = str(pid) + '.db'
        self._db = sqlite3.connect(database=fileName, check_same_thread=False)
        self._db.executescript('''CREATE TABLE IF NOT EXISTS POSTPAGE (
            PAGE INTEGER PRIMARY KEY NOT NULL,
            RES BLOB NOT NULL
        );
        CREATE TABLE IF NOT EXISTS MAINFLOOR (
            FLOOR INTEGER PRIMARY KEY NOT NULL,
            REPLYID INTEGER NOT NULL,
            PUBTIME INTEGER NOT NULL,
            AUTHOR TEXT NOT NULL,
            CONTEXT BLOB NOT NULL
        );
        CREATE TABLE IF NOT EXISTS SUBPAGE (
            REPLYINFO TEXT PRIMARY KEY NOT NULL,
            RES BLOB NOT NULL
        );
        CREATE TABLE IF NOT EXISTS SUBFLOOR (
            PUBTIME INTEGER PRIMARY KEY NOT NULL,
            MAINID INTEGER NOT NULL,
            AUTHOR TEXT NOT NULL,
            CONTEXT BLOB NOT NULL
        );
        CREATE TABLE IF NOT EXISTS USERS (
            USERID INTEGER PRIMARY KEY NOT NULL,
            USERNAME TEXT NOT NULL,
            USERDATA BLOB NOT NULL
        );
        CREATE TABLE IF NOT EXISTS IMAGES (
            LINK TEXT PRIMARY KEY NOT NULL,
            RES BLOB NOT NULL
        )''')

        self.autoCommitFlag = True
        self.__threadLock = threading.Lock()

        def commitTimer():
            while True:
                if self.autoCommitFlag:
                    self.commitNow()
                sleep(2)

        threading._start_new_thread(commitTimer, tuple())

        self.queue = Queue()
        self.getTotalChange = lambda: self._db.total_changes

    def checkExistPage(self, pageNumber: int):
        result = self._db.execute(
            'SELECT PAGE,RES FROM POSTPAGE WHERE PAGE = ?', (pageNumber,))
        resultList = list(result)
        if not resultList:
            return False
        else:
            return resultList[0]

    def writePage(self, pageNumber: int, pageRes: str):
        if self.checkExistPage(pageNumber):
            return False
        self.queue.put(
            ('INSERT INTO POSTPAGE (PAGE,RES) VALUES (?,?)', (pageNumber, pageRes)))

    def checkExistFloor(self, floorNumber: int):
        result = self._db.execute(
            'SELECT FLOOR,REPLYID,PUBTIME,AUTHOR,CONTEXT FROM MAINFLOOR WHERE FLOOR = ?', (floorNumber,))
        result = list(result)
        if not list(result):
            return False
        else:
            return list(result)[0]

    def writeFloor(self, floorNumber: int, replyID: int, publishTime: int, author: str, context: str):
        if self.checkExistFloor(floorNumber):
            return False
        self.queue.put(('INSERT INTO MAINFLOOR (FLOOR,REPLYID,PUBTIME,AUTHOR,CONTEXT) VALUES (?,?,?,?,?)',
                        (floorNumber, replyID, publishTime, author, context)))

    def checkExistSubPage(self, replyInfo: str):
        result = self._db.execute(
            'SELECT REPLYINFO,RES FROM SUBPAGE WHERE REPLYINFO = ?', (replyInfo,))
        result = list(result)
        if not result:
            return False
        else:
            return result[0]

    def writeSubPage(self, replyInfo: str, context: str):
        if self.checkExistSubPage(replyInfo):
            return False
        self.queue.put((
            'INSERT INTO SUBPAGE (REPLYINFO,RES) VALUES (?,?)', (replyInfo, context)))

    def checkExistSubFloor(self, publishTime: int):
        result = self._db.execute(
            'SELECT PUBTIME,MAINID,AUTHOR,CONTEXT FROM SUBFLOOR WHERE PUBTIME = ?', (publishTime,))
        result = list(result)
        if not list(result):
            return False
        else:
            return list(result)[0]

    def writeSubFloor(self, publishTime: int, mainFloorID: int, author: str, context: str):
        if self.checkExistSubFloor(publishTime):
            return False
        self.queue.put(('INSERT INTO SUBFLOOR (PUBTIME,MAINID,AUTHOR,CONTEXT) VALUES (?,?,?,?)',
                        (publishTime, mainFloorID, author, context)))

    def checkExistUsers(self, userID: int):
        result = self._db.execute(
            'SELECT USERID,USERNAME,USERDATA FROM USERS WHERE USERID = ?', (userID,))
        result = list(result)
        if not result:
            return False
        else:
            return result[0]

    def writeUsers(self, userID: int, userName: str, context: str):
        if self.checkExistUsers(userID):
            return False
        self.queue.put((
            'INSERT INTO USERS (USERID,USERNAME,USERDATA) VALUES (?,?,?)', (userID, userName, context)))

    def checkExistImage(self, imageLink: str):
        result = self._db.execute(
            'SELECT LINK,RES FROM IMAGES WHERE LINK = ?', (imageLink,))
        result = list(result)
        if not list(result):
            return False
        else:
            return list(result)[0]

    def writeImage(self, imageLink: str, imageRes: bytes):
        if self.checkExistImage(imageLink):
            return False

        self.queue.put(
            ('INSERT INTO IMAGES (LINK,RES) VALUES (?,?)', (imageLink, imageRes)))

    def executeCommand(self):
        while True:
            self._db.execute(*self.queue.get())
            self.commitNow()
            yield self._db.total_changes

    def commitNow(self):
        self.__threadLock.acquire()
        self._db.commit()
        self.__threadLock.release()
        return self._db.total_changes

    def __del__(self):
        self.commitNow()
        return
