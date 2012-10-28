#!/usr/bin/python
import os 
from pygame import *
from vector2d import *
import math

class GameMap:
	def __init__(self,name):
		self.load(name)

	def load(self,name):
		mapname = os.path.join('maps',name)
		self.game_map = image.load(mapname).convert()
		self.rect = self.game_map.get_rect()
		self.game_map.set_colorkey(Color("Black"))
		self.collision_map = surfarray.array_colorkey(self.game_map)
		self.game_map.set_colorkey(None)
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
	def setScreenStuff(self,screen,screen_rect):
		self.screen = screen
		self.screen_rect = screen_rect

	def show(self):
		self.screen.blit(self.game_map,Rect(0,0,0,0), area=self.screen_rect)

class Board:
	def __init__(self,game_map):
		self.game_map = game_map
		self.players =  [] 
		self.projectiles = []
		self.objects = [] 
		self.gravity = Vector2D(x=0,y=10)

	def epoch(self,):
		"""call me every frame"""

		self._handleObjectCollisions()
		self._handleTerrainCollisions()
		self._handleMovement()
		self._handleAttached()

		for i in self.projectiles:
			i.epoch()
			for j in i.emit():
				self._addEmittedProjectile(j,i)


			if i.unregister():
				self.unregisterProjectile(i)

		for i in self.players:
			i.epoch()

			for j in i.emit():
				self._addEmittedProjectile(j,i)

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

	def _handleAttached(self):
		for i in self.objects:
			for attachement in i.attached:
				attachement.rect.x = i.rect.centerx + attachement.attach_x
				attachement.rect.y = i.rect.centery + attachement.attach_y
				attachement.v = i.v
				attachement.epoch()

				for j in attachement.emit():
					self._addEmittedProjectile(j,attachement)

	def _handleProjectileMovement(self):

		for i in self.projectiles:
			r = i.sprite.rect
			r.x +=v.x
			r.y += v.y

	def _addEmittedProjectile(self,projectile,parent):
			projectile.v+=parent.v
			projectile.x = parent.x
			projectile.y = parent.y
			self.registerProprojectileectile(projectile)

	#mess
	def _handlePlayerMovement(self):
		for i in self.players:
			i.handleForce()
			i.v+=self.gravity
			pixelx = i.rect.centerx
			pixely = i.rect.bottom

			mx=i.v.x+i.forgottenx
			my=i.v.y+i.forgotteny

			movex = int(math.floor(mx))
			movey = int(math.floor(my))

			i.forgottenx = mx - math.floor(mx)
			i.forgotteny = my - math.floor(my)

			mcm = self.game_map.collision_map
			pixels_touched = 0

			while( movex != 0 or movey != 0 ):

				if abs(movex) > 0 and mcm[pixelx][pixely+1]==255:
					pixels_touched+=1

				if movex > 0:

					if pixelx+1 >= self.game_map.rect.right:
						i.v.x = 0 
						movex = 0 

					elif mcm[pixelx+1][pixely] == 0:
						pixelx+=1
						movex-=1

					elif pixely-1 < 0 :
						i.v.x =0 
						movex =0 

					elif mcm[pixelx+1][pixely-1] == 0 and movex>=2:
						movex-=2
						pixelx+=1
						pixely+=1
					else:
						i.forgottenx+=movex
						movex=0
						i.v.x=0 

				if movex < 0:

					if pixelx - 1 <  0 :
						i.v.x=0
						movex = 0 

					elif mcm[pixelx-1][pixely] == 0:
						pixelx-=1
						movex+=1
					elif pixely-1 < 0:
						i.v.x =0 
						movex=0 
					elif mcm[pixelx-1][pixely-1] == 0 and movex<=-2:
						movex-=2
						pixelx-=1
						pixely+=1
					else:
						i.forgottenx+=movex
						movex=0
						i.v.x = 0 

				if movey > 0:
					if pixely +1 >= self.game_map.rect.bottom:
						i.v.y=0
						movey = 0
					elif mcm[pixelx][pixely+1] ==0 :
						pixely+=1
						movey-=1
					else:
						if movey < 2:
							i.forgotteny+=movey
						movey = 0 
						i.v.y = 0
						i.handleTerrainImpact()

				if movey < 0 :
					if pixely - 1 < 0:
						i.v.y = 0 
						movey =0 
					elif mcm[pixelx][pixely-1] == 0 :
						pixely-=1
						movey+=1
					else:
						if movey > -2:
							i.forgotteny+=movey

						movey = 0 
						i.v.y = 0 
						i.handleTerrainImpact()

				
			i.rect.centerx = pixelx 
			i.rect.bottom = pixely  
			i.handleFriction(pixels_touched,self.gravity)


	def _objectsCollide(self,obj1, obj2):

		if not obj1.collides() or not obj2.collides():
			return False

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

		if not obj1.collides():
			return False

		r = obj1.rect
		mcm = self.game_map.collision_map
		cm = obj1.collision_map

		for y in range(0, r.height):
			for x in range(0,r.width):
				if mcm[r.x+x][r.y+y] & cm[x][y]:
					return True

		return False



class BoardObject:
	def __init__(self,x,y,v):
		self.rect=Rect(x,y,666,666)
		self.v = v
		self.force = Vector2D()

	def emit(self):
		"""return a list of emitted projectiles"""
		return []

	def epoch(self):
		""" stuff you would like to do in the game epoch,
		stuff like dying to bullets or creating a harmful explosion """
		return


class AttachableObject(BoardObject):
	def __init__(self,attach_x,attach_y):

		BoardObject.__init__(0,0, Vector2D(0,0))
		self.attach_x = attach_x
		self.attach_y = attach_y


class PhysicalObject(BoardObject):

	def __init__(self,x,y,collision_map, mass=1,v=Vector2D()):

		BoardObject.__init__(self,x,y,v)

		self.forgotteny=0
		self.forgottenx=0
		self.mass=mass


		self.setCollisionMap(collision_map)

		self.v = Vector2D() 
		self.attached = []

	def setCollisionMap(self, collision_map):

		tmprect = collision_map.get_rect()
		tmprect.x = self.rect.x
		tmprect.y = self.rect.y
		self.rect = tmprect
		collision_map.set_colorkey(Color("Black"))
		self.collision_map = surfarray.array_colorkey(collision_map)
		
	def collides(self):
		return True
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
		self.v +=velocity


	def handleFriction(self,pixels,gravity):

		friction = pixels*gravity.y*self.friction
		friction = math.copysign(friction, self.v.x)*-1
		if abs(friction) >= abs(self.v.x):
			self.v.x=0
		else:
			self.v.x+=friction

	def applyForce(self,f):
		"""self explanatory"""
		self.force+=f

	def handleForce(self):
		self.v += self.force/self.mass
		self.force.x=0
		self.force.y=0

	def movable(self):
		"""if you dont want your object to be moved return False"""
		return True

	
	def addCollision(self,obj):
		return

	def unregister(self):
		"""return true if you want to unregister from engine"""
		return False

	def attach(self,obj,x,y):
		self.attached.append(obj)

	def unattach(self,obj):
		self.attached.remove(obj)

