# -*- coding:utf-8 -*-
import Queue
import threading
import urllib,urllib2
import time
#import chardet
from bs4 import BeautifulSoup

queue1 = Queue.Queue()
queue2 = Queue.Queue()

lock = threading.Lock()
fd = open("url.list")
count = 1

class ReadFile(threading.Thread):  
    """Read File and Grasp url put the contents into the queue."""

    def __init__(self, queue ):   
        threading.Thread.__init__(self)
        self.queue = queue
        global fd     
        self.fd = fd
    def run(self):
        while True:
	    if self.queue.qsize() > 1000:
	        pass
	    else :
                lock.acquire()
                host = fd.readline()  # get a line from file.
                lock.release()
                url = urllib2.urlopen(host)
                contents = url.read()
                self.queue.put(contents)  
	    
class AnalyzeHtml(threading.Thread):  
    """ Read the contents from the queue and analyze."""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
	global count
        while True:
	    if self.queue.qsize() < 1:
	        pass
	    else:
                html = self.queue.get()
                #charest = chardet.detect(html)
	        #print charest
                #soup = BeautifulSoup(html,from_encoding=charest['encoding'])
                soup = BeautifulSoup(html)
                soup.findAll(['title'])
		lock.acquire()
		count = count + 1
		if (count == 1000):
		    print '$'*100
		    print (time.time() - start )
		lock.release()
start = time.time()

def main():
    # Start four threads to put html to queue[0|1]:
    for i in range(2):
        print i
        if i % 2 == 0:
            t = ReadFile(queue1)  
	    t.setDaemon(True)
            t.start()
        else:
            s = ReadFile(queue2)
	    s.setDaemon(True)
            s.start()
    # Start two threads to analyze the html from queue[0|1]
    for i in range(2):
        if i % 2 == 0:	
            dt = AnalyzeHtml(queue1)
	    dt.setDaemon(True)
            dt.start()
        else:
            dq = AnalyzeHtml(queue2)
	    dq.setDaemon(True)
            dq.start()

if __name__ == "__main__":
    start = time.time() 
    main()
    while True: 
	try:
	    time.sleep(1)
	except KeyboardInterrupt:
	    break
    print "Time is %s" % (time.time() -start)
