#!/usr/bin/python
from board import *
from vector2d import *
from pygame import *
class Player(BoardObject):
	#dummy
	def __init__(self,x,y,angle, img_name, collision_map_name):
		img_name = os.path.join('img',img_name)
		collision_map_name = os.path.join('img',collision_map_name)

		img = image.load(img_name).convert()
		cm = image.load(collision_map_name).convert()
		BoardObject.__init__(self,x,y,cm)
		self.img = img
		self.angle=angle
		self.leftv = Vector2D(x=-1,y=0)
		self.rightv = Vector2D(x=1,y=0)
		self.jumpv = Vector2D(x=0,y=-40)
		self.jetv = Vector2D(x=0,y=-20)
		self.ground = False

	def handleTerrainImpact(self):
		self.ground = True
		print "terrain impact"
		return False

	def setAngle(self,angle):
		"""sets the weapon angle"""
		pass

	def jump(self):
		if self.ground:
			self.applyVelocity(self.jumpv)

	def moveLeft(self):
		"""moves the character left"""
		self.applyVelocity(self.leftv)

	def moveRight(self):
		"""moves the character right"""
		self.applyVelocity(self.rightv)
		pass

	def jets(self):
		self.applyVelocity(self.jetv)
		"""fires the jets"""
		pass
	def show(self,screen):
		screen.blit(self.img,self.rect)
	
