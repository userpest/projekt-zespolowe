#!/usr/bin/python
import pygame

class Camera:
	def __init__(self):
		self.track=False
		self.objects = []

	def track(self,tracked):
		self.track = True
		self.tracked = tracked

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
			tracked = self.tracked.real_coords_rect
			self.lookAt(tracked.centerx,tracked.centery)

		for i in self.objects:
			i.show()	

		

#messy
camera = Camera()

class CameraObject:

	def __init__(self,img,real_coords_rect):
		self.real_coords_rect = real_coords_rect
		self.camerapos=pygame.Rect(0,0,real_coords_rect.width,real_coords_rect.height)
		self.img = img
		global camera
		camera.register(self)

	def show(self):
		r = self.camerapos
		real_coords_rect = self.real_coords_rect
		r.x = real_coords_rect.x - self.screen_rect.x
		r.y = real_coords_rect.y - self.screen_rect.y
		if ( r.right > 0 and r.left < self.screen_rect.width and r.bottom > 0 and r.top < self.screen_rect.height): 
			self.screen.blit(self.img,r)

	def registerScreen(self, screen,screen_rect):
		self.screen = screen
		self.screen_rect = screen_rect

	def unregister(self):
		global camera
		camera.unregister(self)

