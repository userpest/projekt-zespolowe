#!/usr/bin/python
from board import *
from pygame import *
from math import *
import resourcemanager
import os

class Projectile(PhysicalObject):
	def __init__(self,dmg,owner,x,y,collision_map,img):
		PhysicalObject.__init__(self,x,y,collision_map,img)
		self.dmg = dmg
		self.owner = owner
	def handleCollision(self,obj):
		self.unregister = True
	def handleTerrainImpact(self):
		self.unregister = True
	def handleObjectImpact(self):
		self.unregister = True

class BazookaRocket(Projectile):
	def __init__(self,owner,visible=True):
		self.explosion = False
		img = resourcemanager.get_image(os.path.join('img','weapons','bazooka','rocket.png'))
		cm = resourcemanager.get_image(os.path.join('img','weapons','bazooka','rocket_cm.png'))
		img.set_colorkey(Color("Black"))
		cm.set_colorkey(Color("Red"))

		self.explosion_cm = resourcemanager.get_image(os.path.join('img','weapons','bazooka','explosion_cm.png'))
		self.explosion_img = resourcemanager.get_image(os.path.join('img','weapons','bazooka','explosion.png'))

		self.explosion_cm.set_colorkey(Color("Red"))
		self.explosion_img.set_colorkey(Color("Black"))

		super(BazookaRocket,self).__init__(50,owner,0,0,cm,img)


	def handleCollision(self,obj):
		self.explode()

	def handleTerrainImpact(self):
		self.explode()

	def explode(self):
		if not self.explosion:
			self.explosion = True
			self.movable = False
			self.explosion_timer = 3
			self.setCollisionMap(self.explosion_cm)
			self.img = self.explosion_img


	def epoch(self):
		super(BazookaRocket,self).epoch()
		if self.explosion:
			self.explosion_timer-=1
			if self.explosion_timer == 0 :
				self.unregister = True
		
class Ak47Bullet(Projectile):
	def __init__(self,owner,visible=True):
		img = resourcemanager.get_image(os.path.join('img','weapons','ak47','bullet.png'))
		cm = resourcemanager.get_image(os.path.join('img','weapons','ak47','bullet_collision_map.png'))
		img.set_colorkey(Color("Black"))
		cm.set_colorkey(Color("Red"))
		Projectile.__init__(self,10,owner,0,0,cm,img)
		self.damage=10



#this can make the weapons loadable from config
class Weapon(AttachableObject):

	def __init__(self,owner,attachx, attachy, ammo,ammo_count, exit_r, exit_speed,img_left,img_right,visible = 1 , projectiles_per_round = 1, cooldown = 0, colorkey = Color("Black")):
		"""img should be given for the rotation of 0 degree (as in polar coordinate system just replace radians with degrees ;x) """
		self.img = resourcemanager.get_image(img_right,colorkey=Color("White"))
		AttachableObject.__init__(self,attachx,attachy,self.img,visible)

		self.img_left= img_left
		self.img_right = img_right

		self.ammo_count = ammo_count
		self.magazine_size = ammo_count
		#self.ammo = ammo		
		self.per_round = projectiles_per_round
		self.cooldown = cooldown
		self.cooldown_timer = 0 
		self.angle = 0 
		self.exit_speed = exit_speed
		self.fire =False
		self.projectiles_per_round= projectiles_per_round
		self.radius = exit_r
		self.current_outx, self.current_outy  = self.calc_exit_coords(0)
		self.owner = owner

		self.imgs =[0]*360

		for i in range(-90,90):
			img = resourcemanager.rotate_image(img_right,i)
			img.set_colorkey(colorkey)
			self.imgs[i%360]=img

		for i in range(90,270):
			img = resourcemanager.rotate_image(img_left,i-180)
			img.set_colorkey(colorkey)
			self.imgs[i]= img


	def calc_exit_coords(self,angle):
		return (int(self.radius*cos(angle)),int(self.radius*sin(angle)))

	def reload(self):
		self.ammo_count = self.magazine_size
		
	def emit(self):
		if self.fire and self.cooldown_timer==0 and self.ammo_count > 0 :
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
			
			self.current_outx ,self.current_outy = self.calc_exit_coords(angle)

			angle = 2*pi - angle
			angle_in_deg= int(angle*180/pi)%360
			self.img = self.imgs[angle_in_deg]
#			tmp = self.rect
			self.rect = self.img.get_rect()

#			self.rect.centerx, self.rect.centery= tmp.centerx, tmp.centery

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
	def __init__(self,owner,visible=False):
		self.visible=visible
		img_dir=os.path.join('img','weapons','ak47')
		img_left = os.path.join(img_dir,'ak47_left.png')
		img_right = os.path.join(img_dir, 'ak47_right.png')
		Weapon.__init__(self,owner,0,0,self.shot,100,20,17,img_left,img_right,cooldown=1,colorkey=Color("White"))
	def shot(self):
		return Ak47Bullet(self.visible)

class TestWeapon(AK47):
	def __init__(self,owner,visible=False):
		self.visible=visible
		img_dir=os.path.join('img','weapons','test')
		img_left = os.path.join(img_dir,'test_left.png')
		img_right = os.path.join(img_dir, 'test_right.png')
		Weapon.__init__(self,owner,0,0,self.shot,15,25,17,img_left,img_right,cooldown=10,colorkey=Color("White"))
	def shot(self):
		return Ak47Bullet(self.owner,self.visible)


class Bazooka(Weapon):
	def __init__(self,owner,visible=False):
		self.visible = visible
		img_dir=os.path.join('img','weapons','bazooka')
		img_left = os.path.join(img_dir,'bazooka_left2.png')
		img_right = os.path.join(img_dir, 'bazooka_right2.png')
		Weapon.__init__(self,owner,0,0,self.shot,3,50,12,img_left,img_right,cooldown=50,colorkey=Color("White"))

	def shot(self):
		return BazookaRocket(self.owner,self.visible)
