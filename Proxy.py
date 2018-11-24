from Proxy_Moudle import proxy
from avalon_framework import Avalon
import sqlite3 as sql
import urllib.request as url
import urllib.error as ure
import time,os,re,json

stamp = int(time.time())

while 1 == 1 :
    if time.time() - stamp >= 10:
        proxy.write(proxy.get(161737181321320461576))
        stamp = int(time.time())
    
