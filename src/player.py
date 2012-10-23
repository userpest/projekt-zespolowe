#!/usr/bin/python
from board import *
from vector2d import *
from pygame import *
class Player(PhysicalObject):
	#dummy
	def __init__(self,x,y,angle, img_name, collision_map_name):
		img_name = os.path.join('img',img_name)
		collision_map_name = os.path.join('img',collision_map_name)

		img = image.load(img_name).convert()
		cm = image.load(collision_map_name).convert()

		PhysicalObject.__init__(self,x,y,cm)

		self.img = img
		self.angle=angle
		self.leftv = Vector2D(x=-2,y=0)
		self.rightv = Vector2D(x=2,y=0)
		self.jumpv = Vector2D(x=0,y=-40)
		self.jetv = Vector2D(x=0,y=-20)
		self.xlimit = 5
		self.ylimit = 10
		self.ground = False
		self.friction = 0.02

	def handleTerrainImpact(self):
		self.ground = True
		return False

	def setAngle(self,angle):
		"""sets the weapon angle"""
		pass

	def jump(self):
		if self.ground:
			self.applyVelocity(self.jumpv)
			self.ground = False

	def moveLeft(self):
		
		"""moves the character left"""
		self.applyVelocity(self.leftv)

	def moveRight(self):
		"""moves the character right"""
		self.applyVelocity(self.rightv)

	def jets(self):
		"""fires the jets"""
		self.applyVelocity(self.jetv)
		self.ground = False
	def show(self,screen):
		screen.blit(self.img,self.rect)
	
