#!/usr/bin/python

import pygame
from player import *
from board import *


screen = pygame.display.set_mode((468, 60))

plyr = Player(0,0,0,"hero.png", "hero.png")
gm = GameMap("map.jpg")
engine = Board(gm)

while 1:
	engine.epoch()
	engine.registerPlayer(plyr)
	gm.show(screen)	
	plyr.show(screen)
	pygame.display.flip()

	pygame.time.wait(50)
