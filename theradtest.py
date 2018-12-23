from avalon_framework import Avalon
from Spider import posts
from Image import image
from Database import database
from Markdown import markdown
import threading,queue,time,os

postsGetExit = imagesGetExit = imagesUploadExit =False
postsThreadList = imagesThreadList = imagesUpThreadList =[]
postLink = 'https://tieba.baidu.com/p/%s?see_lz=1&pn=' % (1766018024)
threadNum = 4

postsQueueLock = threading.Lock()
postsWorkQueue = queue.Queue(-1)
class postsGetThread(threading.Thread):
    def __init__(self, id, q):
        threading.Thread.__init__(self)
        self.id = id
        self.q = q
    
    def run(self):
        Avalon.info('Start Thread %s to get posts.' % (str(self.id)))
        behavior.postsGet(self.q,self.id)
        Avalon.info('Thread %s Ended.' % (str(self.id)))

imagesQueueLock = threading.Lock()
imagesWorkQueue = queue.Queue(-1)
class imagesGetThread(threading.Thread):
    def __init__(self, id, q):
        threading.Thread.__init__(self)
        self.id = id
        self.q = q
    
    def run(self):
        Avalon.info('Start Thread %s to get images.' % (str(self.id)))
        behavior.imagesGet(self.q,self.id)
        Avalon.info('Thread %s Ended.' % (str(self.id)))

imagesUpQueueLock = threading.Lock()
imagesUpWorkQueue = queue.Queue(-1)
class imagesUploadThread(threading.Thread):
    def __init__(self, id, q):
        threading.Thread.__init__(self)
        self.id = id
        self.q = q
    
    def run(self):
        Avalon.info('Start Thread %s to upload images.' % (str(self.id)))
        behavior.imagesUpload(self.q,self.id)
        Avalon.info('Thread %s Ended' % (str(self.id)))

class behavior:
    def postsGet(q,id):
        while not postsGetExit:
            postsQueueLock.acquire()
            if not postsWorkQueue.empty():
                data = q.get()
                tid = id
                Avalon.info('Thread %s start download page %s.' % (str(tid),str(data[1])))
                postsQueueLock.release()
                resource = posts.getPost(data[0])
                #print(resource,data[1])
                print(database.postWrite(resource,data[1]))
            else:
                postsQueueLock.release()
            time.sleep(1)
    
    def imagesGet(q,id):
        while not imagesGetExit:
            imagesQueueLock.acquire()
            if not imagesWorkQueue.empty():
                data = q.get()
                tid = id
                Avalon.info('Thread %s start download picture %s.' % (str(tid),str((data.spilt('/')[-1]))))
                imagesQueueLock.release()
                resource = image.get(data)
                print(database.imageWrite(resource,data))
            else:
                imagesQueueLock.release()
            time.sleep(1)
    
    def imagesUpload(q,id):
        while not imagesUploadExit:
            imagesUpQueueLock.acquire()
            if not imagesUpWorkQueue.empty():
                data = int(q.get())
                tid = id
                Avalon.info('Thread %s start upload picture(database ID:%s).' % (str(tid),str(data)))
                imagesUpQueueLock.release()
                resource = database.imageRead_id(data)
                link = image.bedUpload(resource)
                print(database.imageLinkUpdate(data,link))
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

postsQueueLock.acquire()
Avalon.info('Start Program')
for pageNumber in range(1,posts.pageNumber(posts.getPost(postLink + '1')) + 1):
    link = postLink + str(pageNumber)
    postsWorkQueue.put([link,pageNumber])
postsQueueLock.release()

while not postsWorkQueue.empty():
    time.sleep(1)
postsGetExit = True
for t in postsThreadList:
    t.join()
Avalon.info('Program Ended!')