#!/usr/bin/python
from board import *
from vector2d import *
from pygame import *
from camera import *
class Player(PhysicalObject, CameraObject):
	#dummy
	def __init__(self,x,y,angle, img_name, collision_map_name,visible=True):
		img_name = os.path.join('img',img_name)
		collision_map_name = os.path.join('img',collision_map_name)

		img = image.load(img_name).convert()
		cm = image.load(collision_map_name).convert()

		PhysicalObject.__init__(self,x,y,cm)

		self.visible= visible

		if visible:
			CameraObject.__init__(self, img,self.rect)

		self.left = False
		self.right = False
		self.jump = False
		self.jets = False

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

	def epoch(self):
		if self.left:
			self.moveLeft()

		if self.right:
			self.moveRight()

		if self.jump:
			self.performJump()

		if self.jets:
			self.useJets()

	def performJump(self):
		if self.ground:
			self.applyVelocity(self.jumpv)
			self.ground = False

	def moveLeft(self):
		
		"""moves the character left"""
		self.applyVelocity(self.leftv)

	def moveRight(self):
		"""moves the character right"""
		self.applyVelocity(self.rightv)

	def useJets(self):
		"""fires the jets"""
		self.applyVelocity(self.jetv)
		self.ground = False
	
