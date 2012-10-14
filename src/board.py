#!/usr/bin/python
import os 
from pygame import *
from vector2d import *


class GameMap:
	def __init__(self,name):
		self.load(name)

	def load(self,name):
		mapname = os.path.join('maps',name)
		self.game_map = image.load(mapname).convert()
		self.game_map.x = 0 
		self.game_map.y = 0 
		self.collision_map = surfarray.array_colorkey(game_map)
		self.changed = False

	def processProjectile(self, obj):
		#TODO: optimize - this function should modify the collision map only in the place of impact
		self.game_map.blit(obj.img,obj.img.rect)		

	def epoch(self):	
		#TODO: see processProjectile
		if self.changed:
			self.collision_map = surfarray.array_colorkey(game_map)
			self.changed = False

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
				if self._objectsCollide(i,j):
					i.addCollison(j)


	def _handleTerrainCollisions(self):
		for i in self.objects:
			if self._terrainCollision(i):
				if i.handleTerrainImpact():
					self.game_map.processProjectile(i)	
				else:
					#bounce/ calculate impact on movement
					pass


	def _handleMovement():
		pass

	def _objectsCollide(self,obj1, obj2):

		r1 = obj1.sprite.rect
		r2 = obj2.sprite.rect

		overlap = r1.clip(r2)

		cm1 = obj1.img.collision_map
		cm2 = obj2.img.collision_map

		x1 = r1.x-overlap.x	
		y1 = r1.y - overlap.y

		x2 = r2.x-overlap.x 
		y2 = r2.y - overlap.y

		for y in range(0,overlap.height):
			for x in range(0,overlap.width):
				if cm1[x+x1][y+y1] & cm2[x+x2][y+y2]:
					return True

		return False

	def _terrainCollision(self,obj1):
		r = obj1.rect
		mcm = self.game_map.collision_map
		cm = obj1.collision_map

		for y in range(0, r.height):
			for x in range(0,r.width):
				if mcm[r.x+x][r.y+y] & cm[x][y]:
					return True

		return False




class BoardObject:

	def __init__(self,x=None,y=None,img=None, mass=1,v=Vector2D()):

		self.v = v
		self.mass=mass
		self.sprite = sprite.Sprite()

		self.sprite.image = img
		self.sprite.rect = img.get_rect()

		self.sprite.rect.x=x
		self.sprite.rect.y=y

		self.force = Vector2D() 
		self.collision_map = surfarray.array_colorkey(collision_map)

		self.collisions = []

		"""docstring for __init__"""

		pass

	def emit(self):
		"""docstring for emit"""
		pass

	def handleObjectImpact(self):
	 	"""docstring for fname"""
	 	pass

	def handleTerrainImpact(self):
		""" return True to harm some terrain """
		return False

	def setVelocity(self,velocity):
		""" """
		pass

	def applyForce(self,v):
		"""docstring for applyForce"""
		self.force+=v
		pass

	def handleForce(self):
		self.v = self.force/self.mass

	def epoch():
		""" stuff you would like to do in the game epoch, stuff like dying to bullets or creating a harmfull explosion """
		pass
	def addCollision(self,obj):
		self.collisions.append(i)


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

