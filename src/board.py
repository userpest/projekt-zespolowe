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
	def __init__(self,game_map):
		self.game_map = game_map
		self.objects =  [] 

	def epoch(self,):
		"""call me every frame"""
		self._handleObjectCollisions()
		self._handleTerrainCollisions()
		self._handleMovement()


	def register(self, obj):
		"""registers and object in the engine"""
		self.objects.append(obj)
		pass

	def unregister(self, obj):
		"""unregisters an object from the engine """
		self.objects.remove(obj)
		pass


	#TODO: OPTIMIZE
	def _handleObjectCollisions(self):
		for i in self.objects:
			for j in self.objects:
				if self._rectsCollison(i,j) and self._colMapCollision(i,j):
					pass


	def _handleTerrainCollisions(self):
		for i in self.objects:
			if self._terrainCollision(i):
				if i._handleTerrainImpact():
					pass
				else:
					pass


	def _handleMovement():
		pass

	def _rectsCollison(self,obj1, obj2):
		if (obj1.collision_map.get_width() + obj1.x < obj2.x 
			or
		    obj1.x > obj2.collision_map.get_width() + obj2.x  
			or 
	       	    obj1.collision_map.get_height()+obj1.y < obj2.y 
		   	or 
		    obj1.y > obj2.collision_map.get_height() + obj2.y ):

			return False

		return True
	#TODO optimize
	def _colMapCollision(self,obj1,obj2):
		#calculate the overlap coords of the rectangles

		if obj1.collision_map.get_width()+obj1.x > obj2.x:
			collision_start_x = obj2.x
			collision_end_x = obj1.collision_map.get_width()+obj1.x
		else:
			collision_start_x = obj1.x
			collision_end_x = obj2.collision_map.get_width()+obj2.x

		if obj1.collision_map.get_height()+obj1.y > obj2.y:
			collision_start_y = obj2.y
			collision_end_y = obj1.collision_map.get_height()+obj1.y
		else:
			collision_start_y = obj1.y
			collision_end_y = obj2.collision_map.get_height()+obj2.y

		for i in range(


	def _terrainCollision(self,obj1):
		pass




class BoardObject:

	def __init__(self,x=None,y=None,v=Vector2D(),collision_map=None,mass=1):
		self.obj_id=0
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

