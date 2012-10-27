#!/usr/bin/python
import pygame

class CameraObject:

	def __init__(self,real_coords_rect,img):
		self.real_coords_rect = real_coords_rect
		self.rect=pygame.Rect()
		self.img = img

	def show(self):

		r = self.rect
		r.x = real_coords_rect.x - self.screen_rect.x
		r.y = real_coords_rect.y - self.screen_rect.y

		if ( r.x > 0 and r.x < self.screen_rect.width and r.y > 0 and r.y < self.screen_rect.height): 
			screen.blit(self.img,rect)

	def registerScreen(self, screen,screen_rect):
		self.screen = screen
		self.screen_rect = screen_rect

#works under hopeful assumption that map is not smaller than the screen size
class Camera:
	def __init__(self,screen):
		info = pygame.display.Info()
		self.screen_rect =  pygame.Rect( 0, 0, info.current_w, info.current_h)
		self.track=False
		self.objects = []

	def track(self,tracked):
		self.track = True
		self.tracked = tracked

	def untrack(self,tracked):
		self.track = False
		self.tracked= None

	def register(self,obj):
		self.objects.append(obj)		
		obj.registerScreen(self.screen, self.screen_rect)

	def unregister(self,obj):
		self.objects.remove(obj)
	
	def registerMap(self,game_map):
		self.game_map = game_map

	def unregisterMap(self):
		self.game_map = None 

	def show(self,obj):
		if self.track:
			tracked = self.tracked.real_coords_rect
			map_rect = self.game_map.rect
			screen_rect = self.screen_rect

			screen_rect.centerx = tracked.centerx
			screen_rect.centery = tracked.centery

			if screen_rect.left  < map_rect.left:
				screen_rect.left = 0

			if screen_rect.top < map_rect.top:
				screen_rect.top = 0

			if screen_rect.right > map_rect.right:
				screen_rect.right = map_rect.right
			if screen_rect.bottom > map_rect.bottom:
				screen_rect.bottom  = map_rect.bottom 

		for i in self.objects:
			i.show()	
