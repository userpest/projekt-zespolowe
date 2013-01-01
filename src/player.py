#!/usr/bin/python
from board import *
from vector2d import *
from pygame import *
from camera import *
from weapons import *
from bitarray import *
import pickle
import resourcemanager

#if you want the entire class for resync pickle the entire fucker for satan
class Player(PhysicalObject):
	def __init__(self,x,y,angle, img_name, collision_map_name,obj_id = None, visible=True):
		img_name = os.path.join('img',img_name)
		collision_map_name = os.path.join('img',collision_map_name)

		img = resourcemanager.get_image(img_name)
		cm =  resourcemanager.get_image(collision_map_name) 
		PhysicalObject.__init__(self,x,y,cm,img,mass = 1 , visible=visible,obj_id=obj_id)

		self.moves = bitarray([False]*5)
		self.lefti = 0
		self.righti = 1
		self.jumpi = 2
		self.jetsi = 3
		self.firei = 4

		self.img = img
		self.angle=angle
		self.leftv = Vector2D(x=-0.1,y=0)
		self.rightv = Vector2D(x=0.1,y=0)
		self.jumpv = Vector2D(x=0,y=-5)
		self.jetv = Vector2D(x=0,y=-0.2)
		self.xlimit = 5
		self.ylimit = 10
		self.ground = False
		self.friction = 0.02
		self.weapons = [None]*3
		self.weapons[0]=AK47()
		self.weapons[0].visible=False
		self.weapons[1] = TestWeapon()
		self.weapon = self.weapons[1]
		self.attach(self.weapon, self.rect.centerx, self.rect.centery)
		self.weaponnum = 0
	def setWeapon(self,num):
			self.weaponnum = num
			self.unattach(self.weapon)
			self.weapon = self.weapons[num]
			self.attach(self.weapon, 0, 0)

	def handleTerrainImpact(self):
			self.ground = True


	def setAngle(self,angle):
		"""sets the weapon angle"""
		self.weapon.setAngle(angle)


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
	@property
	def left(self):
		return self.moves[self.lefti]
	@left.setter
	def left(self,v):
		self.moves[self.lefti]=v
	@property
	def right(self):
		return self.moves[self.righti]
	@right.setter
	def right(self,v):
		self.moves[self.righti]=v
	@property
	def jump(self):
		return self.moves[self.jumpi]
	@jump.setter
	def jump(self,v):
		self.moves[self.jumpi]=v
	@property
	def jets(self):
		return self.moves[self.jetsi]
	@jets.setter
	def jets(self,v):
		self.moves[self.jetsi]=v
	@property
	def fire(self):
		return self.moves[self.firei]
	@fire.setter
	def fire(self,v):
		self.moves[self.firei]=v
		self.weapon.fire=v

	def getMoves(self):
		return pickle.dumps([self.moves.tobytes(),self.weaponnum,self.weapon.angle])

	def setMoves(self,data):
		d = pickle.loads(data)
		self.moves.frombytes(data[0])
		self.weaponnum = data[1]
		self.setWeapon(self.weaponnum)
		self.weapon.fire=self.moves[self.firei]
		self.weapon.angle = data[2]
