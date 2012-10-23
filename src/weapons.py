#!/usr/bin/python
from board import *
from pygame import *
from math import *

class Bullet(PhysicalObject):
	def __init__(self,angle):
		self.angle = angle

class Weapon(AttachableObject):

	def __init__(self,attachx, attachy, ammo,ammo_count, exit_coords, exit_speed,img,   projectiles_per_round = 1, cooldown = 0 ):
		"""img should be given for the rotation of 0 degree (as in polar coordinate system just replace radians with degrees ;x) """

		AttachableObject.__init__(self,attachx,attachy)

		self.ammo_count = ammo_count
		self.ammo = ammo		
		self.per_round = per_round
		self.cooldown = cooldown
		self.cooldown_timer = 0 
		self.angle = 0 
		self.outx, self.outy = exit_coords
		self.exit_speed = exit_speed
		self.fire =false
		self.projectiles_per_round= projectiles_per_round

		self.current_outx = self.outx
		self.current_outy = self.outy

		self.img = img
		self.imgs =[img]
		for i in range(1,360):
			self.img.append(transfrom.rotate(img,i))

	def emit(self):
		if self.fire :
			to_emit = [] 

			self.cooldown_timer = self.cooldown

			for i in range(1,self.projectiles_per_round):
				projectile = self.ammo()
				projectile.v = Vector2D(self.exit_speed, self.angle)
				projectile.rect.x = self.current_outx
				projectile.rect.y = self.current_outy

				to_emit.append(projectile)

			self.ammo_count-=self.projectiles_per_round
			self.fire = False

			return to_emit


	def epoch(self):
		if self.cooldown_timer > 0:
			self.cooldown_timer-=1

	def fire(self):
		if self.cooldown_timer == 0 :
			self.fire = True

	def setAngle(self,angle):
		if self.angle != angle:
			self.angle = angle
			self.current_outx = int(self.outx*cos(angle))
			self.current_outy = int(self.outy*sin(angle))
			self.img = self.imgs[ int(angle/pi*180) ] 
			

class AK47(Weapon):
	def __init__(self):

