'''
Proxy Get Moudle(Don't Use it alone)
Editor:mnixry
©2014-2018 Mix Tecnology
'''

from avalon_framework import *
import urllib.request as url
import urllib.error as ure
import sqlite3 as sql
import os,json,re,time

if os.path.exists('proxy.db') == False:
    Avalon.warning('Proxy database not exist,program will creat one.')
    try:
        db = sql.connect('proxy.db')
        dbfile = db.cursor()
    except:
        Avalon.error('Has error happen when creating database of proxy!',True)
        raise Exception('Has error happen when creating database of proxy!')
        quit()
    try:
        dbfile.execute('''CREATE TABLE PROXY(
                ID INT PRIMARY KEY NOT NULL,
                IP TEXT NOT NULL,
                PORT TEXT NOT NULL,
                GEO TEXT NOT NULL,
                UPDTIME INT NOT NULL,
                STATUS INT
            );''')
        db.commit()
    except:
        Avalon.error('Has error happen when creating tables of database!',True)
        raise Exception('Has error happen when creating tables of database!')
        quit()
    db.close()

Avalon.info('Opening Database...')

try:
    db = sql.connect('proxy.db',10.0)
    dbfile = db.cursor()
except:
    Avalon.error('Has error happen while opening database of proxy!',True)
    raise Exception('Has error happen while opening database of proxy!')
    quit()

Avalon.info("Database load success!")

class proxy():
    def get(appid):
        try_times = 0
        try:
            proxy = url.urlopen('https://proxy.horocn.com/api/free-proxy?format=json&loc_name=%E4%B8%AD%E5%9B%BD&app_id=' + str(appid))
        except ure.HTTPError as status:
            Avalon.error("Can't Connect to proxy site,Code: %s ." % (status.code()))
            quit()
        proxy = json.loads((proxy.read()).decode())
        return(proxy)

#161737181321320461576

    def proccess(raw,line):
        i = raw[line]
        try:
            id = int((((dbfile.execute('SELECT ID FROM PROXY')).fetchall())[-1])[0]) + 1
        except:
            id = 1
        ip = str(i.get('host'))
        port = int(i.get('port'))
        geo = str('%s,%s,%s' % (i.get('country_cn'),i.get('province_cn'),i.get('city_cn')))
        time = int(i.get('updated_at'))
        return(id,ip,port,geo,time)

    def write(raw):
        for line in range(0,10):
            proxy_list = proxy.proccess(raw,line)
            proxy_list_exist = dbfile.execute("SELECT IP, PORT FROM PROXY WHERE IP == ? AND PORT == ?",(str(proxy_list[1]),int(proxy_list[2])))
            try:
                proxy_list_exist = (proxy_list_exist.fetchall())[0]
            except:
                dbfile.execute('''INSERT INTO PROXY (ID,IP,PORT,GEO,UPDTIME) VALUES (?,?,?,?,?)''',proxy_list)
                db.commit()

#database_write(proxy_raw)