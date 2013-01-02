from threading import *

class ThreadSafeArray:
        def __init__(self):
                self.array = []
                self.lock = Lock()
        def add(self,value):
                self.lock.acquire(True)
                self.array.append(value)
                self.lock.release()
        def remove(self, i):
                self.lock.acquire(True)
                self.array.remove(i)
                self.lock.release()
        def get(self,index):
                return self.array[i]
        def action(self,action,args):
                self.lock.acquire(True)
                action(args)
                self.lock.release()
        def action_method(self,action,obj,args):
                self.lock.acquire(True)
                action(obj,args)
                self.lock.release()
        def get_list(self):
                return self.array
        def get_lenght(self):
                return len(self.array)
        def pop(self,obj):
                self.lock.acquire(True)
                to_pop=-1
                i=0
                for o in self.array:
                        if o==obj:
                                to_pop=i
                                break
                        i = i+1
                if to_pop != -1:
                        to_pop = self.array.pop(to_pop)
                else:
                        to_pop = None
                self.lock.release()
                return to_pop

