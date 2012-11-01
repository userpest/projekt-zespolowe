#!/usr/bin/python
from board import *
from pygame import *
from math import *
import resourcemanager

class Ak47Bullet(PhysicalObject):
	def __init__(self,visible):
		PhysicalObject()
	def damage(self):
		return 10	
	def handleTerrainImpact
	def unregister(self):
		if


def Ak47Bullet(PhysicalObject):
	def __init__(self):

	def damage(self):

#this can make the weapons loadable from config
class Weapon(AttachableObject):

	def __init__(self,attachx, attachy, ammo,ammo_count, exit_coords, exit_speed,img_left,img_right,visible = 1 , projectiles_per_round = 1, cooldown = 0 ):
		"""img should be given for the rotation of 0 degree (as in polar coordinate system just replace radians with degrees ;x) """

		AttachableObject.__init__(self,attachx,attachy,visible)

		self.img_left= img_left
		self.img_right = img_right

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

		self.img = resourcemanager.get_image(img_right)
		self.imgs =[0]*360

		for i in range(-90,90):
			self.img[i%360]=resourcemanager.rotate_image(img_right,i)

		for i in range(90,270):
			self.img[i]=resourcemanager.rotate_image(img_left,i)



	def emit(self):
		if self.fire and self.cooldown_timer==0:
			to_emit = [] 

			self.cooldown_timer = self.cooldown

			for i in range(1,self.projectiles_per_round):
				projectile = self.ammo()
				projectile.v = Vector2D(self.exit_speed, self.angle)
				projectile.rect.x = self.current_outx
				projectile.rect.y = self.current_outy

				to_emit.append(projectile)

			self.ammo_count-=self.projectiles_per_round

			return to_emit


	def epoch(self):
		if self.cooldown_timer > 0:
			self.cooldown_timer-=1

	def setAngle(self,angle):
		if self.angle != angle:
			self.angle = angle
			self.current_outx = int(self.outx*cos(angle))
			self.current_outy = int(self.outy*sin(angle))

			angle = 2*pi - angle
			angle_in_deg= int(angle*180/pi)%360
			self.img = self.imgs[angle] 
			
	def __del__(self):
		img_right = self.img_right
		img_left = self.img_left
		for i in range(-90,90):
			self.img[i%360]=resourcemanager.free(img_right,i)

		for i in range(90,270):
			self.img[i]=resourcemanager.free(img_left,i)


class AK47(Weapon):
	def __init__(self):

