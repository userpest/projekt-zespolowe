#!/usr/bin/python
from board import *
from pygame import *
from math import *
import resourcemanager
import os

class Ak47Bullet(PhysicalObject):
	def __init__(self,visible):
		img = resourcemanager.get_image(os.path.join('img','weapons','ak47','bullet.png'))
		cm = resourcemanager.get_image(os.path.join('img','weapons','ak47','bullet_collision_map.png'))
		img.set_colorkey(Color("Black"))
		cm.set_colorkey(Color("Red"))
		PhysicalObject.__init__(self,0,0,cm,img)
		self.damage=10
	def die(self):
		self.unregister=True
	def handleTerrainImpact(self):
		self.die()
	def handleObjectImpact(self):
		self.die()


#this can make the weapons loadable from config
class Weapon(AttachableObject):

	def __init__(self,attachx, attachy, ammo,ammo_count, exit_coords, exit_speed,img_left,img_right,visible = 1 , projectiles_per_round = 1, cooldown = 0, colorkey = Color("Black")):
		"""img should be given for the rotation of 0 degree (as in polar coordinate system just replace radians with degrees ;x) """
		self.img = resourcemanager.get_image(img_right,colorkey=Color("White"))
		AttachableObject.__init__(self,attachx,attachy,self.img,visible)

		self.img_left= img_left
		self.img_right = img_right

		self.ammo_count = ammo_count
		#self.ammo = ammo		
		self.per_round = projectiles_per_round
		self.cooldown = cooldown
		self.cooldown_timer = 0 
		self.angle = 0 
		self.outx, self.outy = exit_coords
		self.exit_speed = exit_speed
		self.fire =False
		self.projectiles_per_round= projectiles_per_round

		self.current_outx = self.outx
		self.current_outy = self.outy

		self.imgs =[0]*360

		for i in range(-90,90):
			img = resourcemanager.rotate_image(img_right,i)
			img.set_colorkey(colorkey)
			self.imgs[i%360]=img

		for i in range(90,270):
			img = resourcemanager.rotate_image(img_left,i-180)
			img.set_colorkey(colorkey)
			self.imgs[i]= img



	def emit(self):
		if self.fire and self.cooldown_timer==0:
			to_emit = []

			self.cooldown_timer = self.cooldown

			for i in range(0,self.projectiles_per_round):
				#projectile = self.ammo()
				projectile = self.shot()
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
			self.img = self.imgs[angle_in_deg]

	def __del__(self):
		img_right = self.img_right
		img_left = self.img_left
		for i in range(-90,90):
			self.img[i%360]=resourcemanager.free(img_right,i)

		for i in range(90,270):
			self.img[i]=resourcemanager.free(img_left,i)
	#pseudo virtual fucntion
	def shot(self):
		pass
class AK47(Weapon):
	def __init__(self,visible=True):
		self.visible=visible
		img_dir=os.path.join('img','weapons','ak47')
		img_left = os.path.join(img_dir,'ak47_left.png')
		img_right = os.path.join(img_dir, 'ak47_right.png')
		Weapon.__init__(self,0,0,self.shot,100,(20,0),17,img_left,img_right,cooldown=1,colorkey=Color("White"))
	def shot(self):
		return Ak47Bullet(self.visible)
