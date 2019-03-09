from threading import Lock

threadLock = Lock()

def fakePrint(*args, **kwargs):
    threadLock.acquire()
    print(*args, **kwargs)
    threadLock.release()