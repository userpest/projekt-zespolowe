#!/usr/bin/python

import pygame

class EventCallback:
	def __init__(self):
		self.callbacks = {}

	def processEvents(self):
		for event in pygame.event.get(): 
			for callback in self.callbacks[event]:
				callback()

	def registerCallback(self,callback, trigger):
		if trigger not in self.callbacks:
			self.callbacks[trigger]=[]

		self.callbacks[trigger].append(callback)

	def unreagisterCallback(self,callback,trigger):
		if trigger in self.callbacks:
			return

		self.callbacks[trigger].remove(callback)
