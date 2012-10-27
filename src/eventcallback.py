#!/usr/bin/python

import pygame

class EventCallback:
	def __init__(self):
		self.callbacks = {}

	def processEvents(self):
		for event in pygame.event.get(): 
			for callback in self.callbacks[event]:
				callback(event)

	def registerCallback(self, trigger,callback):
		if trigger not in self.callbacks:
			self.callbacks[trigger]=[]

		self.callbacks[trigger].append(callback)

	def unreagisterCallback(self,trigger,callback):
		if trigger not in self.callbacks:
			return

		self.callbacks[trigger].remove(callback)
