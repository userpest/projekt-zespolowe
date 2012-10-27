import pygame

class KeyboardController:
	#TODO: maybe parse some config
	def __init__(self,event_callback,player):
		self.event_callback= event_callback
		self.move_left_key =pygame.K_a
		self.move_right_key = pygame.K_d
		self.jump_key = pygame.K_w
		self.jets_key = pygame.K_SPACE
		
		event_callback.registerCallback(pygame.KEYUP, self.keyUp)
		event.callback.registerCallback(pygame.KEYDOWN, self.keyDown)

		
	def keyDown(self,event):

		if event.key == self.move_left_key:
			self.player.left = True
		if event.key == self.move_right_key:
			self.player.right = True
		if event.key == self.jump_key:
			self.player.jump = True
		if event.key == self.jets_key:
			self.player.jets = True

	def keyUp(self,event):

		if event.key == self.move_left_key:
			self.player.left = False
		if event.key == self.move_right_key:
			self.player.right = False
		if event.key == self.jump_key:
			self.player.jump = False
		if event.key == self.jets_key:
			self.player.jets = False

	def close(self):
		event_callback.unregisterCallback(pygame.KEYUP, self.keyUp)
		event.callback.unregisterCallback(pygame.KEYDOWN, self.keyDown)
