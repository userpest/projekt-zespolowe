#!/usr/bin/python
import os 
import pygame
from vector2d import *


class GameMap:
	def __init__(self,name):
		self.load(name)
	def load(self,name):
		mapname = os.path.join('maps',name)
		self.game_map = pygame.image.load(mapname)
		pass
	def processProjectile(self):
		pass

class Board:
	def __init__(self):
		pass

	def epoch(self,):
		pass


class BoardObject:

	def __init__(self,x=None,y=None,v=Vector2D(),collision_map=None,mass=1):
		self.v = v
		self.mass=mass
		self.x = x
		self.y = y
		self.force = Vector2D() 
		self.collision_map = collision_map
		"""docstring for __init__"""
		pass

	def show(self):
		"""docstring for show"""
		pass

	def emit(self):
		"""docstring for emit"""
		pass

	def handleObjectImpact(self):
	 	"""docstring for fname"""
	 	pass

	def handleTerrainImpact(self):
		""" """
		pass

	def setVelocity(self,velocity):
		""" """
		pass

	def applyForce(self,v):
		"""docstring for applyForce"""
		self.force+=v
		pass

	def epoch():
		self.v


class Player(BoardObject):

	def __init__(self,x=0,y=0,angle=0):
		self.x=x
		self.y=y
		self.angle=angle
		pass

	def setAngle(self,angle):
		"""sets the weapon angle"""
		pass

	def jump(self):
		pass

	def moveLeft(self):
		"""moves the character left"""
		pass

	def moveRight(self):
		"""moves the character right"""
		pass

	def jets(self):
		"""fires the jets"""
		pass

