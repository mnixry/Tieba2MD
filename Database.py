import sqlite3
import json
from threading import _start_new_thread
from time import sleep


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
        CREATE TABLE IF NOT EXISTS SUBFLOOR (
            PUBTIME INTEGER PRIMARY KEY NOT NULL,
            MAINID INTEGER NOT NULL,
            AUTHOR TEXT NOT NULL,
            CONTEXT BLOB NOT NULL
        );
        CREATE TABLE IF NOT EXISTS IMAGES (
            LINK TEXT PRIMARY KEY NOT NULL,
            RES BLOB NOT NULL
        )''')

        def commitTimer():
            while True:
                self._db.commit()
                sleep(5)

        _start_new_thread(commitTimer, tuple())

    def checkExistPage(self, pageNumber: int):
        result = self._db.execute(
            'SELECT PAGE,RES FROM POSTPAGE WHERE PAGE = ?', (pageNumber,))
        resultList = list(result)
        # print(str(resultList)[0:50])
        if not resultList:
            return False
        else:
            return resultList[0]

    def writePage(self, pageNumber: int, pageRes: str):
        if self.checkExistPage(pageNumber):
            return False
        self._db.execute(
            'INSERT INTO POSTPAGE (PAGE,RES) VALUES (?,?)', (pageNumber, pageRes))
        return self._db.total_changes

    def checkExistFloor(self, floorNumber: int):
        result = self._db.execute(
            'SELECT FLOOR,REPLYID,PUBTIME,AUTHOR,CONTEXT FROM MAINFLOOR WHERE PAGE = ?;', (floorNumber,))
        if not list(result):
            return False
        else:
            return list(result)[0]

    def writeFloor(self, floorNumber: int, replyID: int, publishTime: int, author: str, context: str):
        if self.checkExistFloor(floorNumber):
            return False
        self._db.execute('INSERT INTO MAINFLOOR (FLOOR,REPLYID,PUBTIME,AUTHOR,CONTEXT) VALUES (?,?,?,?,?)',
                         (floorNumber, replyID, publishTime, author, context))
        return self._db.total_changes

    def checkExistSubFloor(self, publishTime: int):
        result = self._db.execute(
            'SELECT PUBTIME,MAINID,AUTHOR,CONTEXT FROM SUBFLOOR WHERE PUBTIME = ?', (publishTime,))
        if not list(result):
            return False
        else:
            return list(result)[0]

    def writeSubFloor(self, publishTime: int, mainFloorID: int, author: str, context: str):
        if self.checkExistSubFloor(publishTime):
            return False
        self._db.execute('INSERT INTO SUBFLOOR (PUBTIME,MAINID,AUTHOR,CONTEXT) VALUES (?,?,?,?)',
                         (publishTime, mainFloorID, author, context))
        return self._db.total_changes

    def checkExistImage(self, imageLink: str):
        result = self._db.execute(
            'SELECT LINK,RES FROM IMAGES WHERE LINK = ?', (imageLink,))
        if not list(result):
            return False
        else:
            return list(result)[0]

    def writeImage(self, imageLink: str, imageRes: bytes):
        if self.checkExistImage(imageLink):
            return False
        self._db.execute(
            'INSERT INTO IMAGES (LINK,RES) VALUES (?,?)', (imageLink, imageRes))
        return self._db.total_changes
