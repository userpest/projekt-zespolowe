#!/usr/bin/python

import pygame
from player import *
from board import *


screen = pygame.display.set_mode((800, 600))

plr = Player(0,0,0,"hero.png", "hero.png")
gm = GameMap("map.png")
engine = Board(gm)
engine.registerPlayer(plr)

while 1:
	for event in event.get():

			
	engine.epoch()


	gm.show(screen)	
	plr.show(screen)

	pygame.display.flip()

	pygame.time.wait(50)
