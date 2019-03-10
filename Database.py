import sqlite3
import json


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
            CONTEXT BLOB NOT NULL
        );
        CREATE TABLE IF NOT EXISTS SUBFLOOR (
            PUBTIME INTEGER PRIMARY KEY NOT NULL,
            MAINID INTEGER NOT NULL,
            CONTEXT BLOB NOT NULL
        );
        CREATE TABLE IF NOT EXISTS IMAGES (
            LINK TEXT PRIMARY KEY NOT NULL,
            RES BLOB NOT NULL
        )''')

    def checkExistPage(self, pageNumber: int):
        result = self._db.execute(
            'SELECT (PAGE,RES) FROM POSTPAGE WHERE PAGE = ?;', (pageNumber,))
        if not list(result):
            return False
        else:
            return list(result)[0]

    def writePage(self, pageNumber: int, pageRes: str):
        if self.checkExistPage(pageNumber):
            return False
        self._db.execute(
            'INSERT INTO POSTPAGE (PAGE,RES) VALUE (?,?)', (pageNumber, pageRes))
        return self._db.total_changes

    def checkExistFloor(self, floorNumber: int):
        result = self._db.execute(
            'SELECT (FLOOR,REPLYID,PUBTIME,CONTEXT) FROM MAINFLOOR WHERE PAGE = ?;', (floorNumber,))
        if not list(result):
            return False
        else:
            return list(result)[0]

    def writeFloor(self, floorNumber: int, replyID: int, publishTime: int, context: str):
        if self.checkExistFloor(floorNumber):
            return False
        self._db.execute('INSERT INTO MAINFLOOR (FLOOR,REPLYID,PUBTIME,CONTEXT) VALUE (?,?,?,?)',
                         (floorNumber, replyID, publishTime, context))
        return self._db.total_changes

    def checkExistSubFloor(self, publishTime: int):
        result = self._db.execute(
            'SELECT (PUBTIME,MAINID,CONTEXT) FROM SUBFLOOR WHERE PUBTIME = ?', (publishTime,))
        if not list(result):
            return False
        else:
            return list(result)[0]

    def writeSubFloor(self, publishTime: int, mainFloorID: int, context: str):
        if self.checkExistSubFloor(publishTime):
            return False
        self._db.execute('INSERT INTO SUBFLOOR (PUBTIME,MAINID,CONTEXT) VALUE (?,?,?)',
                         (publishTime, mainFloorID, context))
        return self._db.total_changes

    def checkExistImage(self, imageLink: str):
        result = self._db.execute(
            'SELECT (LINK,RES) FROM IMAGES WHERE LINK = ?', (imageLink,))
        if not list(result):
            return False
        else:
            return list(result)[0]

    def writeImage(self, imageLink: str, imageRes: bytes):
        if self.checkExistImage(imageLink):
            return False
        self._db.execute(
            'INSERT INTO IMAGES (LINK,RES) VALUE (?,?)', (imageLink, imageRes))
        return self._db.total_changes
