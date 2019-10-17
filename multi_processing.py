from multiprocessing import Process, Lock
from time import sleep

class testMultiProcessing:
    def __init__(self):
        self.myLock = Lock()
        pass

    def multiFunction(self, pName, l):
        l.acquire()
        print(pName)
        sleep(1.0)
        l.release()

def pMethod1(obj, lock):
    for i in range(1, 10):
        obj.multiFunction("Process 1", lock)

def pMethod2(obj, lock):
    for i in range(1, 10):
        obj.multiFunction("Process 2", lock)

def spawnProcess():
    obj = testMultiProcessing()
    lock = Lock()

    p1 = Process(target=pMethod1, args=(obj, lock))
    p1.start()
    p2 = Process(target=pMethod2, args=(obj, lock))
    p2.start()


    print("P1 and P2 started. Wait till they finish.")
    sleep(10)
    #p1.join()
    #p2.join()

    print("App finished")

# if __name__ == '__main__':
spawnProcess()