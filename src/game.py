#!/usr/bin/python

import pygame
from player import *
from board import *
import sys


screen = pygame.display.set_mode((800, 600))

player = Player(0,0,0,"hero.png", "hero.png")
gm = GameMap("map.png")
engine = Board(gm)
engine.registerPlayer(player)

while 1:
	sys.exit(1)

	engine.epoch()


	gm.show(screen)	
	player.show(screen)

	pygame.display.flip()

	pygame.time.wait(50)
