import threading

class new(object):
	class SmartThread(object):
		def __init__(self, max_threads):
			self.max_threads = max_threads
			self.tasksQueue = []
		
		def tasksQueueLoop(self, main_connection):
			while main_connection.open:
				if threading.active_count() < self.max_threads and self.tasksQueue != []:
					next_task = self.tasksQueue.pop(0)
					
					threading.Thread(*next_task[0], **next_task[1]).start()
		
		def runParallelTask(self, *args, **kwargs):
			if threading.active_count() < self.max_threads:
				threading.Thread(*args, **kwargs).start()
			
			else:
				self.tasksQueue.append([args, kwargs])