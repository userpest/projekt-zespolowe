#!/usr/bin/python

import pygame

class EventCallback:
	def __init__(self):
		#could use a normal list for speed
		self.callbacks = {}

	def processEvents(self):
		for event in pygame.event.get(): 
			if event.type in self.callbacks:
				for callback in self.callbacks[event.type]:
					callback(event)

	def registerCallback(self, trigger,callback):
		if trigger not in self.callbacks:
			self.callbacks[trigger]=[]

		self.callbacks[trigger].append(callback)

	def unreagisterCallback(self,trigger,callback):
		if trigger not in self.callbacks:
			return

		self.callbacks[trigger].remove(callback)
