#/usr/local/env python3
#__coding:utf-8 __
'''
Baidu Tieba Downloader Main Program.

fllowed GPL license.
'''
from Markdown import *
from Spider import *
from avalon_framework import *
import os

#need something here
#Test line

while True:
    link = Avalon.gets('Please input Link:\n[?]:')
    try:
        pid = int((link.split('/'))[-1].split('?')[0])
    except:
        Avalon.warning('Invaild Input!')
        pass
    else:
        pid = str(pid)
        Avalon.info('PID:' + pid)
        break

see_lz = Avalon.ask('Only Download Floor owner?',True)

if see_lz:
    therad_link = 'https://tieba.baidu.com/p/%s?see_lz=1&pn=' % (pid)
    Avalon.info('Mode:Only Download Floor Owner')
else:
    therad_link = 'https://tieba.baidu.com/p/%s?pn=' % (pid)
    Avalon.info('Mode:Download all')

while True:
    filename = Avalon.gets('Please input filename/filepath and filename:\n[?]:')
    if filename.split('.')[-1] != 'md':
        Avalon.warning('Filename Error!')
    try:
        file = open(filename,'w+',1,'utf-8')
    except:
        Avalon.warning('Filename Error!')
        pass
    else:
        break

for page_number in range(1,posts.page_num(posts.get(therad_link + '1')) + 1):
    Avalon.time_info('Start Page ' + str(page_number))
    raw = posts.get(therad_link + str(page_number))
    for per_floor in posts.proccess(raw):
        #print(per_floor)
        file.write(Markdown.convert(per_floor))
    #print('\n')

file.close()