#/usr/local/env python3
#__coding:utf-8 __
'''
Save Downloaded data to Database.

fllowed GPL license.
'''

from avalon_framework import Avalon
import sqlite3 as sql
import os,random,time,html,_thread

if os.path.isfile('Database.db'):
    os.remove('Database.db')

_db = sql.connect('Database.db',check_same_thread=False)
_dbCursor = _db.cursor()
_db.execute('''CREATE TABLE RES(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,PN INT NOT NULL,RES BLOB NOT NULL);''')
_db.execute('''CREATE TABLE IMAGES(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,ORIGIN TEXT NOT NULL,IMG BLOB NOT NULL,NEW TEXT);''')
_db.commit()

class database():
    
    def postWrite(raw,pageNumber):
        for i in range(1,6):
            try:
                _dbCursor.execute('''INSERT INTO RES (PN,RES) VALUES (?,?);''',(pageNumber,raw))
            except sql.Error as status:
                Avalon.warning('Database error at Page %s!Reason:%s.(%s/5)' % (str(pageNumber),str(status),str(i)))
            else:
                break
        else:
            Avalon.error('Database error happen when writing page %s!' % (str(pageNumber)))
        try:
            id = _dbCursor.execute('''SELECT ID FROM RES;''')[-1]
        except:
            id = _db.total_changes
        _db.commit()
        return(id)

    def postRead(pageNumber):
        for i in range(1,6):
            try:
                res = _dbCursor.execute('''SELECT RES FROM RES WHERE PN=?;''',pageNumber)[0]
            except sql.Error as status:
                Avalon.warning('Database error at Page %s!Reason:%s.(%s/5)' % (str(pageNumber),str(status),str(i)))
            else:
                break
        else:
            Avalon.error('Database error happen when reading page %s!' % (str(pageNumber)))
        return(res)

    def imageWrite(raw,link):
        for i in range(1,6):
            try:
                _dbCursor.execute('''INSERT INTO IMAGES (LINK,RES) VALUES (?,?);''',(link,raw))
            except sql.Error as status:
                Avalon.warning('Database error!Reason:%s.(%s/5)' % (str(status),str(i)))
            else:
                break
        else:
            Avalon.error('Database error happen when writing images.')
        try:
            id = _dbCursor.execute('''SELECT ID FROM IMAGES;''')[-1]
        except:
            id = _db.total_changes
        _db.commit()
        return(id)

    def imageRead_id(id):
        raw = _dbCursor.execute('''SELECT IMG FROM IMAGES WHERE ID=?;''',int(id))[0]
        return(raw)

    def imageRead_link(originLink):
        raw = _dbCursor.execute('''SELECT IMG FROM IMAGES WHERE ORIGIN=?;''',str(originLink))[0]
        return(raw)

    def imageLinkUpdate(id,newLink):
        _dbCursor.execute('''UPDATE IMAGES SET NEW = ? WHERE ID=?;''',(str(newLink),int(id)))
        _db.commit()
        return(_db.total_changes)