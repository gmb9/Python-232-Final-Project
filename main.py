import math
import random

import pygame
from pygame import mixer

pygame.init()

#Screen and Background
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background.png')

#Caption and Icon
pygame.display.set_caption("Wild West Duel")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('player.png')
playerX = 100
playerY = 300
playerX_change = 0
playery_change = 0

#Enemy
enemyImg = pygame.image.load('enemy.png')
enemyX = 600
enemyY = 300
enemyX_change = 0
enemyY_change = 0

#Game Over Text

over_font = pygame.font.Font('freesansbold.ttf, 64')

#Music
#mixer.music.load("background.wav")
#mixer.music.play(-1)

def display(img, x, y):
    screen.blit(img, (x, y))

def game_over_text():
    over_text = over_font.render("You Lose...", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display(playerImg, playerX, playerY)
    display(enemyImg, enemyX, enemyY)
    pygame.display.update()