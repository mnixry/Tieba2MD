#/usr/local/env python3
#__coding:utf-8 __
'''
Save Downloaded data to Database.

fllowed GPL license.
'''

from avalon_framework import Avalon
import sqlite3 as sql
import os
import random
import time
import html
import _thread


class database():

    def __init__(self, filename='Database.db'):
        if os.path.isfile(filename):
            os.remove(filename)
        self.__db = sql.connect(filename, check_same_thread=False)
        self.__db.execute(
            '''CREATE TABLE RES(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,PN INT NOT NULL,RES BLOB NOT NULL);''')
        self.__db.execute(
            '''CREATE TABLE IMAGES(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,ORIGIN TEXT NOT NULL,IMG BLOB NOT NULL,NEW TEXT);''')
        self.__db.commit()

    def postWrite(self, raw, pageNumber):
        for i in range(1, 6):
            try:
                self.__db.execute(
                    '''INSERT INTO RES (PN,RES) VALUES (?,?);''', (pageNumber, raw))
            except sql.Error as status:
                Avalon.warning('Database error at Page %s!Reason:%s.(%s/5)' %
                               (str(pageNumber), str(status), str(i)))
            else:
                break
        else:
            Avalon.error('Database error happen when writing page %s!' %
                         (str(pageNumber)))
        try:
            id = self.__db.execute('''SELECT ID FROM RES;''')[-1]
        except:
            id = self.__db.total_changes
        self.__db.commit()
        return(id)

    def postRead(self, pageNumber):
        for i in range(1, 6):
            try:
                res = self.__db.execute(
                    '''SELECT RES FROM RES WHERE PN=?;''', pageNumber)[0]
            except sql.Error as status:
                Avalon.warning('Database error at Page %s!Reason:%s.(%s/5)' %
                               (str(pageNumber), str(status), str(i)))
            else:
                break
        else:
            Avalon.error('Database error happen when reading page %s!' %
                         (str(pageNumber)))
        return(res)

    def imageWrite(self, raw, link):
        for i in range(1, 6):
            try:
                self.__db.execute(
                    '''INSERT INTO IMAGES (LINK,RES) VALUES (?,?);''', (link, raw))
            except sql.Error as status:
                Avalon.warning('Database error!Reason:%s.(%s/5)' %
                               (str(status), str(i)))
            else:
                break
        else:
            Avalon.error('Database error happen when writing images.')
        try:
            id = self.__db.execute('''SELECT ID FROM IMAGES;''')[-1]
        except:
            id = self.__db.total_changes
        self.__db.commit()
        return(id)

    def imageRead_id(self, id):
        raw = self.__db.execute(
            '''SELECT IMG FROM IMAGES WHERE ID=?;''', int(id))[0]
        return(raw)

    def imageRead_link(self, originLink):
        raw = self.__db.execute(
            '''SELECT IMG FROM IMAGES WHERE ORIGIN=?;''', str(originLink))[0]
        return(raw)

    def imageLinkUpdate(self, id, newLink):
        self.__db.execute(
            '''UPDATE IMAGES SET NEW = ? WHERE ID=?;''', (str(newLink), int(id)))
        self.__db.commit()
        return(self.__db.total_changes)
