#!/usr/bin/python2.7

import pygame
from player import *
from board import *
from camera import camera
from eventcallback import *
from keyboardcontroller import *
from crosshair import *
import sys


def quit(event):
	pygame.quit()
	sys.exit(1)


screen = pygame.display.set_mode((800, 600))
camera.setScreen()

player = Player(0,0,0,"hero.png", "hero.png")
gm = GameMap("map.png")
engine = Board(gm)
camera.registerMap(gm)
engine.registerPlayer(player)

event_callback = EventCallback()
crosshair = Crosshair("crosshair.png",player,event_callback)
keyboard = KeyboardController(player,event_callback)
event_callback.registerCallback(pygame.QUIT, quit)
camera.trackObject(player)

while 1:

	event_callback.processEvents()
	crosshair.epoch()
	engine.epoch()
	camera.show()
	crosshair.show()
	pygame.display.flip()

	pygame.time.wait(16)
