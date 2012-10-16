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
		self.collision_map = surfarray.array_colorkey(self.game_map)
		self.changed = False

	def processProjectile(self, obj):
		#TODO: optimize - this function should modify the collision map only in the place of impact
		self.game_map.blit(obj.img,obj.img.rect)		

		r = obj.rect
		mcm = self.collision_map
		cm = obj.collision_map

		for y in range(0, r.height):
			for x in range(0,r.width):
				if mcm[r.x+x][r.y+y] & cm[x][y]:
					mcm[r.x+x][r.y+y]=0
		
	#	self.changed = True

	def epoch(self):	
		#TODO: see processProjectile
	#	if self.changed:
	#		self.collision_map = surfarray.array_colorkey(game_map)
	#		self.changed = False
		pass
	def show(self,screen):
		screen.blit(self.game_map,(0,0))

class Board:
	def __init__(self,game_map):
		self.game_map = game_map
		self.players =  [] 
		self.projectiles = []
		self.objects = [] 

	def epoch(self,):
		"""call me every frame"""

		self._handleObjectCollisions()
		self._handleTerrainCollisions()
		self._handleMovement()

		for i in self.projectiles:
			i.epoch()
			if i.unregister():
				self.unregisterProjectile(i)

		for i in self.players:
			i.epoch()

			if i.unregister():
				self.unregisterPlayer(i)

	def registerPlayer(self, obj):
		self.players.append(obj)
		self.objects.append(obj)

	def unregisterPlayer(self,obj):
		self.players.remove(obj)
		self.objects.remove(obj)

	def registerProjectile(self,obj):
		self.projectiles.append(obj)
		self.objects.append(obj)

	def unregisterProjectile(self, obj):
		self.projectiles.remove(obj)
		self.objects.remove(obj)


	#TODO: OPTIMIZE
	def _handleObjectCollisions(self):
		for i in self.objects:
			for j in self.objects:
				if self._objectsCollide(i,j):
					i.addCollision(j)


	def _handleTerrainCollisions(self):
		for i in self.projectiles:
			if i.movable() and self._terrainCollision(i):
				self.game_map.processProjectile(i)	
				i.handleTerrainImpact()


	def _handleMovement(self):

		self._handlePlayerMovement()
		self._handleProjectileMovement()

	def _handleProjectileMovement(self):

		for i in self.projectiles:
			r = i.sprite.rect
			r.x +=v.x
			r.y += v.y

	def _handlePlayerMovement(self):
		for i in self.players:
			i.handleForce()
			#apply gravity TODO: ugly
			i.v.y-=10
			pixelx = i.rect.centerx
			pixely = i.rect.bottom
			movex = int(i.v.x)
			movey = int(i.v.y)

			mcm = self.game_map.collision_map

			while( movex != 0 or movey != 0 ):

				if movex > 0:
					if mcm[pixelx+1][pixely] == 0:
						pixelx+=1
						movex-=1
					elif mcm[pixelx+1][pixely+1] == 0 and movex>=2:
						movex-=2
						pixelx+=1
						pixely+=1
					else:
						movex=0
						i.v.x=0 

				if movex < 0:
					if mcm[pixelx+1][pixely] == 0:
						pixelx-=1
						movex+=1
					elif mcm[pixelx+1][pixely+1] == 0 and movex<=-2:
						movex-=2
						pixelx-=1
						pixely+=1
					else:
						movex=0
						i.v.x = 0 

				if movey > 0:
					if mcm[pixelx][pixely+1] ==0 :
						pixely+=1
						movey-=1
					else:
						movey = 0 
						i.v.y = 0
						i.handleTerrainImpact()

				if movey < 0 :
					if mcm[pixelx][pixely-1] == 0 :
						pixely-=1
						movey+=1
					else:
						movey = 0 
						i.v.y = 0 
						i.handleTerrainImpact()


	def _objectsCollide(self,obj1, obj2):

		r1 = obj1.rect
		r2 = obj2.rect

		overlap = r1.clip(r2)

		cm1 = obj1.collision_map
		cm2 = obj2.collision_map

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

	def __init__(self,x,y,collision_map, mass=1,v=Vector2D()):

		self.v = v
		self.mass=mass

		self.rect = Rect(x,y,666,666)

		self.setCollisionMap(collision_map)

		self.force = Vector2D() 

	def setCollisionMap(self, collision_map):

		tmprect = collision_map.get_rect()
		tmprect.x = self.rect.x
		tmprect.y = self.rect.y
		self.rect = tmprect
		self.collision_map = surfarray.array_colorkey(collision_map)
		

	def handleObjectImpact(self):
	 	"""return something youd like to pass to the other object, 
		like the harm you do to it"""
		return None

	def handleTerrainImpact(self):
		""" callback on terrain impact"""
		return

	def setVelocity(self,velocity):
		"""self explanatory """
		self.v = velocity

	def applyVelocity(self,velocity):
		self.v +=v

	def applyForce(self,v):
		"""self explanatory"""
		self.force+=v

	def handleForce(self):
		self.v = self.force/self.mass

	def movable(self):
		"""if you dont want your object to be moved return False"""
		return True

	def epoch(self):
		""" stuff you would like to do in the game epoch,
		stuff like dying to bullets or creating a harmful explosion """
		return

	def addCollision(self,obj):
		return

	def unregister(self):
		"""return true if you want to unregister from engine"""
		return False

