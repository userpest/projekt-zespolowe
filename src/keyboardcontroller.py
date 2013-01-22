import pygame

class KeyboardController(object):
	#TODO: maybe parse some config
	def __init__(self,player,event_callback):
		self.player= player
		self.event_callback= event_callback
		self.move_left_key =pygame.K_a
		self.move_right_key = pygame.K_d
		self.jump_key = pygame.K_w
		self.jets_key = pygame.K_SPACE
		self.weapon_1 = pygame.K_1
		self.weapon_2 = pygame.K_2
		self.reload_weapon = pygame.K_r
		
		event_callback.registerCallback(pygame.KEYUP, self.keyUp)
		event_callback.registerCallback(pygame.KEYDOWN, self.keyDown)

		
	def keyDown(self,event):

		if event.key == self.move_left_key:
			self.player.left = True
		if event.key == self.move_right_key:
			self.player.right = True
		if event.key == self.jump_key:
			self.player.jump = True
		if event.key == self.jets_key:
			self.player.jets = True
		if event.key == self.weapon_1:
			self.player.setWeapon(1)
		if event.key == self.weapon_2:
			self.player.setWeapon(2)
		if event.key == self.reload_weapon:
			self.player.weapon.reload()

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
		self.event_callback.unregisterCallback(pygame.KEYUP, self.keyUp)
		self.event_callback.unregisterCallback(pygame.KEYDOWN, self.keyDown)

