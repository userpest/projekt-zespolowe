from threading import *
from socket import *
import pygame
import json
import copy_reg
import types

timeout=0.5
buffsize=2048
img_format="RGBA"

def CreateSocket():
    sock=socket(AF_INET,SOCK_DGRAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    return sock
def CreateSocketTcp():
	sock=socket(AF_INET,SOCK_STREAM)
	return sock	
def patch_copy_reg():
	copy_reg.pickle(pygame.Surface,__dumps_surface,__loads_surface)	
	#copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)


def __dumps_surface(surface):
	size = json.dumps(surface.get_size())
	img = pygame.image.tostring(surface,img_format)
	return __loads_surface, (size,img)

def __loads_surface(size,img):
	return pygame.image.fromstring(img,json.loads(size),img_format)




def _pickle_method(method):
	"""
	Pickle methods properly, including class methods.
	"""
	func_name = method.im_func.__name__
	obj = method.im_self
	cls = method.im_class
	if isinstance(cls, type):
	        # handle classmethods differently
	        cls = obj
	        obj = None
	if func_name.startswith('__') and not func_name.endswith('__'):
        	#deal with mangled names
	        cls_name = cls.__name__.lstrip('_')
	        func_name = '_%s%s' % (cls_name, func_name)

	return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
	"""
	Unpickle methods properly, including class methods.
	"""
	if obj is None:
	        return cls.__dict__[func_name].__get__(obj, cls)
	for cls in cls.__mro__:
	        try:
        		func = cls.__dict__[func_name]
		except KeyError:
	            pass
	        else:
        	    break
	return func.__get__(obj, cls)
