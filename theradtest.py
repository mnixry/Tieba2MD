from avalon_framework import Avalon
from Spider import posts
from Image import image
from Database import database
from markdown import markdown
import threading,queue,time,os

postsGetExit = imagesGetExit = imagesUploadExit =False
postsThreadList = imagesThreadList = imagesUpThreadList =[]
postsQueueLock = imagesQueueLock = imagesUpQueueLock = threading.Lock()
postsWorkQueue = imagesWorkQueue = imagesUpWorkQueue = queue.Queue(-1)
threadNum = 4

class postsGetThread(threading.Thread):
    def __init__(self, id, q):
        threading.Thread.__init__(self)
        self.id = id
        self.q = q
    
    def run(self):
        Avalon.info('Start Thread %s to get posts.' % (str(self.id)))
        time.sleep(1)
        behavior.postsGet(self.q,self.id)
        time.sleep(1)
        Avalon.info('Thread %s Ended.' % (str(self.id)))

class imagesGetThread(threading.Thread):
    def __init__(self, id, q):
        threading.Thread.__init__(self)
        self.id = id
        self.q = q
    
    def run(self):
        Avalon.info('Start Thread %s to get images.' % (str(self.id)))
        time.sleep(1)
        behavior.imagesGet(self.q,self.id)
        time.sleep(1)
        Avalon.info('Thread %s Ended.' % (str(self.id)))

class imagesUploadThread(threading.Thread):
    def __init__(self, id, q):
        threading.Thread.__init__(self)
        self.id = id
        self.q = q
    
    def run(self):
        Avalon.info('Start Thread %s to upload images.' % (str(self.id)))
        time.sleep(1)
        behavior.imagesUpload(self.q,self.id)
        time.sleep(1)
        Avalon.info('Thread %s Ended' % (str(self.id)))

class behavior:
    def postsGet(q,id):
        while not postsGetExit:
            postsQueueLock.acquire()
            if not postsWorkQueue.empty():
                data = q.get()
                tid = id.get()
                postsQueueLock.release()
                Avalon.info('Thread %s start download page %s.' % (str(tid),str(data[1])))
                time.sleep(1)
                resource = posts.getPost(data[0])
                database.postWrite(resource,data[1])
            else:
                postsQueueLock.release()
            time.sleep(1)
    
    def imagesGet(q,id):
        while not imagesGetExit:
            imagesQueueLock.acquire()
            if not imagesWorkQueue.empty():
                data = q.get()
                tid = id.get()
                imagesQueueLock.release()
                Avalon.info('Thread %s start download picture %s.' % (str(tid),str((data.spilt('/')[-1]))))
                time.sleep(1)
                resource = image.get(data)
                database.imageWrite(resource,data)
            else:
                imagesQueueLock.release()
            time.sleep(1)
    
    def imagesUpload(q,id):
        while not imagesUploadExit:
            imagesUpQueueLock.acquire()
            if not imagesUpWorkQueue.empty():
                data = int(q.get())
                tid = id.get()
                imagesUpQueueLock.release()
                Avalon.info('Thread %s start upload picture(database ID:%s).' % (str(tid),str(data)))
                time.sleep(1)
                resource = database.imageRead_id(data)
                link = image.bedUpload(resource)
                database.imageLinkUpdate(data,link)
            else:
                imagesUpQueueLock.release()
            time.sleep(1)

for ThreadID in range(0,threadNum):
    thread = postsGetThread(ThreadID + 1,postsWorkQueue)
    thread.start()
    postsThreadList.append(thread)

for ThreadID in range(0,threadNum):
    thread = imagesGetThread(ThreadID + 1,postsWorkQueue)
    thread.start()
    imagesThreadList.append(thread)

for ThreadID in range(0,threadNum):
    thread = imagesUploadThread(ThreadID + 1,postsWorkQueue)
    thread.start()
    imagesUpThreadList.append(thread)