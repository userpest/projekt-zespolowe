import threeading
import time


class Ticker:
	def __init__(self,function,args,sleep_time,obj=None):
		self.function = function
		self.args = args
		self.sleep_time = sleep_time
		self.obj = obj
		self.not_end = False
	def run(self):
		Thread(target=self.__running,args=(self,)).start()
	def __running(self):
		self.not_end = True
		while self.not_end:
			if self.obj !=None:
				self.function(self.obj,self.args)
			else:
				self.function(self.args)
			time.sleep(self.time_sleep)
	def stop(self):
		self.not_end = False	
