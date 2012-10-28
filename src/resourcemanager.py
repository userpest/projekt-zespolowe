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
	if cache[name][angle]==None :
		img = get_image(name)
		__cache[name][angle] = transfrom.rotate(img,angle)

	return rotation_cache[name][angle]
