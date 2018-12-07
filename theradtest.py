from avalon_framework import Avalon
from Database import database
from Spider import posts
from Markdown import markdown
from Image import image
import os,queue,threading,_thread,time

exitFlag = False
queueLock = threading.Lock()
workQueue = queue.Queue(4)
theradList = ['1','2','3','4']
therads = []

class postTherad(threading.Thread):
    def __init__(self, id, q):
        threading.Thread.__init__(self)
        self.id = id
        self.q = q
    def run(self):
        Avalon.info('Start post thread %s.\n' % (str(self.id)))
        getPost(self.id,self.q)
        Avalon.info('Post thread %s stopped.\n' % (str(self.id)))

class imageTherad(threading.Thread):
    def __init__(self, id, link):
        threading.Thread.__init__(self)
        self.id = id
        self.link = link
    def run(self):
        Avalon.info('Start image thread %s.' % (str(self.id)))
        getImage(self.id,self.q)
        Avalon.info('Image thread %s stopped.' % (str(self.id)))

def getPost(id,q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            tid = id.get()
            q = q.get()
            link = q[0]
            pageNumber = q[1]
            queueLock.release()
            Avalon.info('Therad No.%s Proccessing %s' % (str(tid),str(pageNumber)))
            raw = posts.getPost(link)
            database.postWrite(raw,pageNumber)
        else:
            queueLock.release()
        time.sleep(1)

def getImage(id,q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            link = q.get()
            queueLock.release()
            raw = image.get(link)
            database.imageWrite(raw,link)
        else:
            queueLock.release()
        time.sleep(1)

pagelink = []
for pageNumber in range(1,posts.pageNumber(posts.getPost('https://tieba.baidu.com/p/3363856719?see_lz=1&pn=' + '1')) + 1):
    link = 'https://tieba.baidu.com/p/3363856719?see_lz=1&pn=' + str(pageNumber)
    pn = pageNumber
    pagelink.append((link,pn))

for theradID in theradList:
    therad = postTherad(theradID,pagelink)
    therad.start()
    therads.append(therad)

queueLock.acquire()
for q in pagelink:
    workQueue.put(q)
queueLock.release()

while not workQueue.empty():
    pass
exitFlag = True

for t in therads:
    t.join()