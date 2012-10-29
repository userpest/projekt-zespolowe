#!/usr/bin/python
from pygame import *


__cache = {}

def get_image(name, force_reload = False):

	if name not in __cache or force_reload :
		load(name)

	return __cache[name][0]

def unload(name):
	__cache[name] = [None]*360

def load(name):
	unload(name)
	__cache[name][0]=image.load(name).convert()

def clear():
	__cache = {}

def rotate_image(name,angle):

	img = get_image(name)

	if cache[name][angle]==None :
		__cache[name][angle] = transform.rotate(img,angle)

	return __cache[name][angle]
