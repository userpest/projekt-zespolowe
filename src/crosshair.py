#!/usr/bin/python

import pygame
from Vector2D import *

#TODO: add different movement speeds
class Crosshair:
	def __init__(self,screen, img_path,player, event_callback):
		pygame.mouse.set_visible(False)
		self.img = image.load(img_path).convert()
		self.img.set_colorkey(pygame.Color("Black"))
		self.player=player
		self.event_callback = event_callback
		event_callback.registerCallback(pygame.MOUSEBUTTONDOWN, self.startFire)
		event_callback.registerCallback(pygame.MOUSEBUTTONUP, self.stopFire)
		event_callback.registerCallback(pygame.MOUSEMOTION, self.move)
		self.x_unitary = Vector2D(1,0)
		self.rect=img.get_rect()
		self.rect.centerx,self.rect.centery = pygame.mouse.get_pos()

	def show(screen):
		screen.blit(self.img,self.rect)

	def calculateAngle(self,posx,posy):
		self.v.setByCoords(self.rect.centerx-player.camera.x, self.rect.centery-player.camera.y)
		player.setAngle(self.v.dotAngle(self.x_unitary))

	def close(self):
		pygame.mouse.set_visible(True)
		event_callback = self.event_callback
		event_callback.unregisterCallback(pygame.MOUSEBUTTONDOWN, self.startFire)
		event_callback.unregisterCallback(pygame.MOUSEBUTTONUP, self.stopFire)
		event_callback.unregisterCallback(pygame.MOUSEMOTION, self.move)

	def move(self,event):
		x,y = event.pos
		self.rect.x = x
		self.rect.y = y
		self.calculateAngle()	

	def startFire(self,event):
		self.player.fire = True
	def stopFire(self,event):
		self.player.fire = False

