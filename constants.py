import pygame

"""
A set of constants for the python roguelike tutorial game.
"""
pygame.init()
#Game sizes
GAME_WIDTH = 800
GAME_HEIGHT = 600
CELL_WIDTH = 32
CELL_HEIGHT = 32

#MAP VARS
MAP_WIDTH = 20
MAP_HEIGHT = 20

#Color definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)

#Game colors
COLOR_DEFAULT_BG = COLOR_GREY

#SPRITES
S_PLAYER = pygame.image.load("sprites/player.png")
S_ENEMY = pygame.image.load("sprites/crab.png")
S_WALL = pygame.image.load("sprites/wall.jpg")
S_FLOOR = pygame.image.load("sprites/floor.png")
#Map
