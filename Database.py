#/usr/local/env python3
#__coding:utf-8 __
'''
Save Downloaded data to Database.

fllowed GPL license.
'''

import sqlite3 as sql
import os,random,time,html

if os.path.isfile('Database.db'):
    os.remove('Database.db')

_db = sql.connect('Database.db')
_db.execute('''CREATE TABLE RES(ID INT PRIMARY KEY NOT NULL,PN INT NOT NULL,RES BLOB NOT NULL);''')
_db.execute('''CREATE TABLE IMAGES(ID INT PRIMARY KEY NOT NULL,ORIGIN TEXT NOT NULL,IMG BLOB NOT NULL,NEW TEXT);''')
_db.commit()

class database():
    
    def postWrite(raw,pageNumber):
        cursor = _db.cursor()
        cursor.execute('''INSERT INTO RES (PN,RES) VALUES (?,?);''',(pageNumber,raw))
        cursor.commit()
        id = cursor.execute('''SELECT ID FROM RES;''')[-1]
        return(id)

    def postRead(pageNumber):
        cursor = _db.cursor()
        res = cursor.execute('''SELECT RES FROM RES WHERE PN=?;''',pageNumber)[0]
        return(res)

    def imageWrite(raw,link):
        cursor = _db.cursor()
        cursor.execute('''INSERT INTO IMAGES (LINK,RES) VALUES (?,?);''',(link,raw))
        cursor.commit()
        id = cursor.execute('''SELECT ID FROM IMAGES;''')[-1]
        return(id)

    def imageRead_id(id):
        cursor = _db.cursor()
        raw = cursor.execute('''SELECT IMG FROM IMAGES WHERE ID=?;''',int(id))[0]
        return(raw)

    def imageRead_link(originLink):
        cursor = _db.cursor()
        raw = cursor.execute('''SELECT IMG FROM IMAGES WHERE ORIGIN=?;''',str(originLink))[0]
        return(raw)

    def imageLinkUpdate(originLink,newLink):
        cursor = _db.cursor()
        cursor.execute('''UPDATE IMAGES SET NEW = ? WHERE ORIGIN=?;''',(str(newLink),str(originLink)))
        cursor.commit()
        return(_db.total_changes)