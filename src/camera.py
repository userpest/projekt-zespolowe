#!/usr/bin/python
import pygame
import weakref
class Camera(object):
	def __init__(self):
		self.track=False
		self.objects = []

	def trackObject(self,tracked):
		self.track = True
		self.tracked = weakref.proxy(tracked)

	def untrack(self,tracked):
		self.track = False
		self.tracked= None

	def setScreen(self):
		info = pygame.display.Info()
		self.screen = pygame.display.get_surface()
		self.screen_rect =  pygame.Rect( 0, 0, info.current_w, info.current_h)

	def reset(self):
		self.screen = None
		self.screen_rect = None
		self.track = False
		self.tracked = None
		self.objects = [] 

	def lookAt(self,x,y):

		map_rect = self.game_map.rect
		screen_rect = self.screen_rect

		screen_rect.centerx = x 
		screen_rect.centery = y 

		if screen_rect.left  < map_rect.left:
			screen_rect.left = 0

		if screen_rect.top < map_rect.top:
			screen_rect.top = 0

		if screen_rect.right > map_rect.right:
			screen_rect.right = map_rect.right

		if screen_rect.bottom > map_rect.bottom:
			screen_rect.bottom  = map_rect.bottom 

		if screen_rect.width > map_rect.width:
			screen_rect.left=0

		if screen_rect.height > map_rect.height:
			screen_rect.top = 0 

	def register(self,obj):
		self.objects.append(obj)		
		obj.registerScreen(self.screen, self.screen_rect)

	def unregister(self,obj):
		self.objects.remove(obj)
	
	def registerMap(self,game_map):
		self.game_map = game_map
		game_map.setScreenStuff(self.screen, self.screen_rect)

	def unregisterMap(self):
		self.game_map = None 
		

	def show(self):
		self.game_map.show()

		if self.track:
			tracked = self.tracked.rect
			self.lookAt(tracked.centerx,tracked.centery)

		for i in self.objects:
			if i.unregister:
				self.unregister(i)
			else:
				i.show()

	def registerObjects(self,objs):
		for i in objs:
			self.register(i)


		

#messy
camera = Camera()

class CameraObject(object):

	def __init__(self,img,rect,visible = True):
		self.rect = rect
		self.camerapos=pygame.Rect(0,0,rect.width,rect.height)
		self.img = img
		self.unregister = False
		global camera
		camera.register(self)
		self.visible = visible
	def show(self):
		if self.visible:
			r = self.camerapos
			real_coords_rect = self.rect
			r.centerx = real_coords_rect.centerx - self.screen_rect.x
			r.centery = real_coords_rect.centery - self.screen_rect.y
			if ( r.right > 0 and r.left < self.screen_rect.width and r.bottom > 0 and r.top < self.screen_rect.height): 
				self.screen.blit(self.img,r)

	def registerScreen(self, screen,screen_rect):
		self.screen = screen
		self.screen_rect = screen_rect

