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
		self.changed = True

	def epoch(self):	
		#TODO: see processProjectile
		if self.changed:
			self.collision_map = surfarray.array_colorkey(game_map)
			self.changed = False

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


	def registerPlayer(self, obj):
		self.players.append(obj)
		self.objects.append(obj)

	def unregisterPlayer(self,obj)
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
					i.addCollison(j)


	def _handleTerrainCollisions(self):
		for i in self.projectiles:
			if self._terrainCollision(i):
				self.game_map.processProjectile(i)	
				i.handleTerrainImpact():


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
			pixelx = i.sprite.rect.centerx
			pixely = i.sprite.rect.bottom
			movex = int(i.v.x)
			movey = int(i.v.y)

			mcm = self.game_map.collision_map

			while( movex != 0 or movey != 0 ):

				if movex > 0 
					if mcm[pixelx+1][pixely] == 0:
						pixelx+=1
						movex-=1
					else if mcm[pixelx+1][pixely+1] == 0 and movex>=2:
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
					else if mcm[pixelx+1][pixely+1] == 0 and movex<=-2:
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

				if mcm[pixelx][pixely-1] == 0 :
						pixely-=1
						movey+=1
					else:
						movey = 0 
						i.v.y = 0 


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



	def emit(self):
		"""emit some objects like bullets grenades w/e"""
		pass

	def handleObjectImpact(self):
	 	"""return something youd like to pass to the other object, like the harm you do to it"""
		return None

	def handleTerrainImpact(self):
		""" return True to harm some terrain """
		return False

	def setVelocity(self,velocity):
		"""self explanatory """
		self.v = velocity

	def applyForce(self,v):
		"""self explanatory"""
		self.force+=v

	def handleForce(self):
		self.v = self.force/self.mass

	def movable(self):
		"""if you dont want your object to be moved return False"""
		return True

	def epoch(self):
		""" stuff you would like to do in the game epoch, stuff like dying to bullets or creating a harmfull explosion """
		pass

	def addCollision(self,obj):
		pass


class Player(BoardObject):

	def __init__(self,x=0,y=0,angle=0):
		self.x=x
		self.y=y
		self.angle=angle

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

