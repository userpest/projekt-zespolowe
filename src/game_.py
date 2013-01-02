import pygame
from player import *
from board import *
from camera import camera
from eventcallback import *
from keyboardcontroller import *
from crosshair import *
from threading import *
import pickle
import sys
import utils


def quit(event):
	pygame.quit()
	sys.exit(1)

class Game:
	def __init__(self,scrw,scrh,ch_img=None,my_id=-1):
		utils.patch_copy_reg()	
		self.my_id = my_id
		self.screen = pygame.display.set_mode((scrw,scrh))
		camera.setScreen()
		self.event_callback = EventCallback()
		self.event_callback.registerCallback(pygame.QUIT, quit)
		self.crosshair = None
		self.loaded = False
		self.ch_img=ch_img
		self.running = False
	def create(self,map_name):
		self.game_map = GameMap(map_name)
		self.engine = Board(self.game_map)
		camera.registerMap(self.game_map)
	def load(self,date_board):
		self.end()
		if self.loaded:
			camera.unregisterMap()
			self.crosshair.close()
			self.keyboard.close()
		self.engine=pickle.loads(date_board)
		self.game_map=self.engine.getGameMap()
		camera.reset()
		camera.setScreen()
		camera.registerMap(self.game_map)
		camera.registerObjects(self.engine.objects)
		self.set_player_owner(self.my_id,self.ch_img)
		self.loaded = True
		self.start()
	def __running(self):
		self.not_end = True
		self.running = True
		while self.not_end:
			self.event_callback.processEvents()
			if self.crosshair!=None:
				self.crosshair.epoch()
			self.engine.epoch()
			camera.show()
			if self.crosshair!=None:
				 self.crosshair.show()
			pygame.display.flip()
			pygame.time.wait(1000)
		self.running = False
	def start(self,new_thread = True):
		if new_thread:
			Thread(target=Game.__running, args=(self,)).start()
		else:
			self.__running()
	def end(self):
		#self.not_end=False
		while self.running:
			self.not_end = False
	def join_player(self,player):
		self.engine.registerPlayer(player)
	#run after reciving game
	def set_player_owner(self,id_,ch_img):
		self.player = self.engine.getObjectByID(id_)
		self.crosshair = Crosshair(ch_img,self.player,self.event_callback)
		self.keyboard = KeyboardController(self.player,self.event_callback)
		#camera.track(self.player)
	def serialize(self):
		return pickle.dumps(self.engine)

	def getPlayer(self,id_):
		return self.engine.getObjectByID(id_)


"""
uzytkownik dostaje date
tworzy gre z date
gra zawiera juz jego takze
uzytkownik wie jakie ma id, przejmuje kontrole nad ta postacia i ustawia swoj celownik
startuje gra u nieg
"""
