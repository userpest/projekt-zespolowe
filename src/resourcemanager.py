#!/usr/bin/python
from pygame import *


__cache = {}
#thanks to the retardity of weakref
#and my lack of motivation to patch the sources
__refcount = {}

def get_image(name, force_reload = False):

	if name not in __cache or force_reload:
		unload(name)

	if __cache[name][0]==None:
		load(name)
		
	__refcount[name][0]+=1

	return __cache[name][0]

def unload(name):
	__cache[name] = [None]*360
	__refcount[name] = [0]*360

def load(name):
	__cache[name][0]=image.load(name).convert()
	__refcount[name][0]=0

def free(name,angle=0):
	__refcount[name][angle]-=1
	if __refcount[name][angle] == 0:
		__cache[name][angle] == None

def clear():
	__cache = {}
	__refcount == {}

def rotate_image(name,angle):

	if name not in __cache or __cache[name][angle]==None :
		img = get_image(name)
		__cache[name][angle] = transform.rotate(img,angle)

	__refcount[name][angle]+=1
	return __cache[name][angle]
