from avalon_framework import Avalon
from Database import database
from Spider import posts
from Markdown import Markdown
import os,queue,threading,_thread,time

exitFlag = False
queueLock = threading.Lock()
workQueue = queue.Queue(-1)
theradList = ['1','2','3','4']

class postTherad(threading.Thread):
    def __init__(self, id, q, pn):
        threading.Thread.__init__(self)
        self.id = id
        self.pn = pn
    def run(self):
        Avalon.info('Start post thread %s.' % (str(self.id)))
        get_post(self.id,self.q,self.pn)
        Avalon.info('Post thread %s stopped.' % (str(self.id)))

class imageTherad(threading.Thread):
    def __init__(self, id, link):
        threading.Thread.__init__(self)
        self.id = id
        self.link = link
    def run(self):
        Avalon.info('Start image thread %s.' % (str(self.id)))
        get_image(self.id,self.q)
        Avalon.info('Image thread %s stopped.' % (str(self.id)))

def get_post(id,q,pn):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            link = q.get()
            pageNum = pn.get()
            queueLock.release()
            raw = posts.get(link)
            database.post_write(raw,pageNum)
        else:
            queueLock.release()
    time.sleep(1)