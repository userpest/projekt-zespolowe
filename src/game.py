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

move_left_key =pygame.K_a
move_right_key = pygame.K_d
jump_key = pygame.K_w
jets_key = pygame.K_SPACE

left = False
right = False
jump = False
jets = False
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(1)

		if event.type == pygame.KEYDOWN:

			if event.key == move_left_key:
				left = True
			if event.key == move_right_key:
				right = True
			if event.key == jump_key:
				jump = True
			if event.key == jets_key:
				jets = True

		if event.type == pygame.KEYUP:
			if event.key == move_left_key:
				left = False
			if event.key == move_right_key:
				right = False
			if event.key == jump_key:
				jump = False
			if event.key == jets_key:
				jets = False

	if left:
		player.moveLeft()

	if right:
		player.moveRight()
	if jump:
		player.jump()
	if jets:
		player.jets()
			
	engine.epoch()


	gm.show(screen)	
	player.show(screen)

	pygame.display.flip()

	pygame.time.wait(50)
