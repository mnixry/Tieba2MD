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

db = sql.connect('Database.db')
db.execute('''CREATE TABLE RES(ID INT PRIMARY KEY NOT NULL,PN INT NOT NULL,RES BLOB NOT NULL);''')
db.execute('''CREATE TABLE IMAGES(ID INT PRIMARY KEY NOT NULL,ORIGIN TEXT NOT NULL,IMG BLOB NOT NULL,NEW TEXT);''')
db.commit()

class database():
    
    def post_write(raw,page_num):
        db.execute('''INSERT INTO RES (PN,RES) VALUES (?,?);''',(page_num,raw))
        db.commit()
        id = db.execute('''SELECT ID FROM RES;''')[-1]
        return(id)

    def post_read(page_num):
        res = db.execute('''SELECT RES FROM RES WHERE PN == ?;''',page_num)[0]
        return(res)

    def image_write(raw,link):
        db.execute('''INSERT INTO IMAGES (LINK,RES) VALUES (?,?);''',(link,raw))
        db.commit()
        id = db.execute('''SELECT ID FROM IMAGES;''')[-1]
        return(id)