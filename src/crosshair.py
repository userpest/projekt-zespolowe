#!/usr/bin/python

import pygame
import math
from vector2d import *
import os
import  resourcemanager

#TODO: add different movement speeds
class Crosshair:
	def __init__(self, img_name,player, event_callback):

		self.screen = pygame.display.get_surface()
		pygame.mouse.set_visible(False)
		self.setCrosshair(img_name)
		self.player=player
		self.event_callback = event_callback
		event_callback.registerCallback(pygame.MOUSEBUTTONDOWN, self.startFire)
		event_callback.registerCallback(pygame.MOUSEBUTTONUP, self.stopFire)
		event_callback.registerCallback(pygame.MOUSEMOTION, self.move)
		self.x_unitary = Vector2D(x=1,y=0)
		self.v = Vector2D(0,0)

	def setCrosshair(self,img_name):
		img_path = os.path.join('img',img_name)
		self.img = resourcemanager.get_image(img_path)
		self.img.set_colorkey(pygame.Color("Black"))
		self.rect=self.img.get_rect()
		self.rect.centerx,self.rect.centery = pygame.mouse.get_pos()

	def show(self):
		self.screen.blit(self.img,self.rect)

	def calculateAngle(self):
		x = self.rect.x- self.player.camerapos.x
		y = self.rect.y - self.player.camerapos.y
		angle = math.atan2(y,x)
		self.player.setAngle(angle)

	def close(self):
		pygame.mouse.set_visible(True)
		event_callback = self.event_callback
		event_callback.unregisterCallback(pygame.MOUSEBUTTONDOWN, self.startFire)
		event_callback.unregisterCallback(pygame.MOUSEBUTTONUP, self.stopFire)
		event_callback.unregisterCallback(pygame.MOUSEMOTION, self.move)

	def epoch(self):
		self.calculateAngle()

	def move(self,event):
		x,y = event.pos
		self.rect.x = x
		self.rect.y = y

	def startFire(self,event):
		self.player.weapon.fire = True
	def stopFire(self,event):
		self.player.weapon.fire = False

