import threading
from queue import Queue
import time

print_lock = threading.Lock()
#reffing locking ability of threading module. each time something wants to use the print funcition, checks if there is a print_lock on it
#helps avoid data corruption (if print 2+ things at same time, can merge them/fuck up the data)

def exampleJob(worker):
	time.sleep(0.5)

	with print_lock:
		print(threading.current_thread().name,worker) #when done with this, will release print_lock

def threader():
	while True:
		worker = q.get()
		exampleJob(worker)
		q.task_done()

q = Queue()

#job assignment
for x in range(10): 
	t = threading.Thread(target = threader)
	#define threads and targets of them

	t.daemon = True
	#classifying as daemon.. will die when main thread dies. 
	t.start()

start = time.time()
#how many jobs
for worker in range(20): # with 10 workers working on this job
	#20 instances for workers is what its saying
	q.put(worker) #putting worker to queue... duh

q.join() #waits until thread will terminate

print('Entire job took:',time.time() - start)