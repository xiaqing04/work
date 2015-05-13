<<<<<<< HEAD
# -*- coding:utf-8 -*-
import Queue
import threading
import urllib,urllib2
import time
import chardet
from bs4 import BeautifulSoup

queue = Queue.Queue(maxsize = 0)
out_queue = Queue.Queue(maxsize = 0)

class ThreadUrl(threading.Thread):  
    """Threaded Url Grab"""

    def __init__(self, queue, out_queue):   
        threading.Thread.__init__(self)
        self.queue = queue
        self.out_queue = out_queue
    def run(self):
        while True:
            #grabs host from queue
	   
	    host = self.queue.get()  
            html = urllib2.urlopen(host).read()
            #place chunk into out queue
            self.out_queue.put(html)  
            #signals to queue job is done
	    print "**********Thread1 is graspping  html*************"
            self.queue.task_done()     
	    
class DatamineThread(threading.Thread):  
	
    def __init__(self, out_queue,i):
        threading.Thread.__init__(self)
        self.out_queue = out_queue
	self.i = i

    def run(self):
        while True:
            #grabs host from queue
            html = self.out_queue.get()
	    print "Thread [ %d ] is anayazing html" % self.i
	  
	    charest = chardet.detect(html)
	    #print charest
            #parse the chunk
            soup = BeautifulSoup(html,from_encoding=charest['encoding'])
            #print soup.findAll(['title'])
            #signals to queue job is done
	   
            self.out_queue.task_done()
start = time.time()
def main():
    #spawn a pool of threads, and pass them queue instance

    print "current has %d threads " % (threading.activeCount() -1 )
    t = ThreadUrl(queue, out_queue)   
    t.setDaemon(True)
    t.start()

    #populate queue with data
    fd = file("url.list")
    for host in fd.readlines():
        queue.put(host)
    fd.close()

    num_threads = 20 # create five threads to analyze the web contents.
    dt = {}
    for i in range(num_threads):
        print i
        dt = DatamineThread(out_queue, i)
	dt.setDaemon(True)
        dt.start()
    print "current has %d threads " % (threading.activeCount() -1 )
    time.sleep(10)
    print "current has %d threads " % (threading.activeCount() -1 )

    #wait on the queue until everything has been processed
    queue.join()  
    out_queue.join()
   

if __name__ == "__main__":
    main()
    print "Elapsed time is %s " % (time.time() - start )
=======
# -*- coding:utf-8 -*-
import Queue
import threading
import urllib,urllib2
import time
import chardet
from bs4 import BeautifulSoup

queue = Queue.Queue(maxsize = 0)
out_queue = Queue.Queue(maxsize = 0)

class ThreadUrl(threading.Thread):  
    """Threaded Url Grab"""

    def __init__(self, queue, out_queue):   
        threading.Thread.__init__(self)
        self.queue = queue
        self.out_queue = out_queue
    def run(self):
        while True:
            #grabs host from queue
	   
	    host = self.queue.get()  
            html = urllib2.urlopen(host).read()
            #place chunk into out queue
            self.out_queue.put(html)  
            #signals to queue job is done
	    print "**********Thread1 is graspping  html*************"
            self.queue.task_done()     
	    
class DatamineThread(threading.Thread):  
	
    def __init__(self, out_queue,i):
        threading.Thread.__init__(self)
        self.out_queue = out_queue
	self.i = i

    def run(self):
        while True:
            #grabs host from queue
            html = self.out_queue.get()
	    print "Thread [ %d ] is anayazing html" % self.i
	  
	    charest = chardet.detect(html)
	    #print charest
            #parse the chunk
            soup = BeautifulSoup(html,from_encoding=charest['encoding'])
            #print soup.findAll(['title'])
            #signals to queue job is done
            self.out_queue.task_done()
start = time.time()
def main():
    #spawn a pool of threads, and pass them queue instance

    print "current has %d threads " % (threading.activeCount() -1 )
    t = ThreadUrl(queue, out_queue)   
    t.setDaemon(True)
    t.start()

    #populate queue with data
    fd = file("url.list")
    for host in fd.readlines():
        queue.put(host)
    fd.close()

    num_threads = 20 # create five threads to analyze the web contents.
    dt = {}
    for i in range(num_threads):
        print i
        dt = DatamineThread(out_queue, i)
	dt.setDaemon(True)
        dt.start()
    print "current has %d threads " % (threading.activeCount() -1 )
    time.sleep(10)
    print "current has %d threads " % (threading.activeCount() -1 )

    #wait on the queue until everything has been processed
    queue.join()  
    out_queue.join()
   

if __name__ == "__main__":
    main()
    print "Elapsed time is %s " % (time.time() - start )
>>>>>>> ec5a9b7c00ecd2f0842f468196ccece0ae6b11be
