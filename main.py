import math
import random

import pygame, sys
from pygame import mixer

pygame.init()


font = pygame.font.SysFont(None, 20)
clock = pygame.time.Clock()
click = False

#Screen and Background
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode((WINDOW_SIZE))
display = pygame.Surface((300, 200))

background = pygame.image.load('background.png')

#Caption and Icon
pygame.display.set_caption("Platformer")
#icon = pygame.image.load('icon.png')
# pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('player.png').convert()
playerImg.set_colorkey((255, 255, 255))

#Tiles
grassImg = pygame.image.load('grass.png')
dirtImg = pygame.image.load('dirt.png')

tiles = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
         ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2','2','2','2'],
         ['0','0','0','0','0','0','0','0','0','0','2','2','0','0','0','0','0','0','0'],
         ['0','0','0','0','0','0','2','2','0','0','0','0','0','0','0','0','0','0','0'],
         ['0','0','2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
         ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
         ['2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2'],
         ['1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1'],
         ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
         ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
         ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
         ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
         ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]

#Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)

#Music
#mixer.music.load("background.wav")
#mixer.music.play(-1)

#def display(img, x, y):
    #screen.blit(img, (x, y))

def game_over_text():
    over_text = over_font.render("You Lose...", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

def menu():
    while True:
        display.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        draw_text('Main Menu', font, (0, 0, 0), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game()

        #if button_2.collidepoint((mx, my)):
        #    if click:
        #        pass


        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pygame.display.update()
        #mainClock.tick(60)

def game():
    vertical_momentum = 0
    moving_right = False
    moving_left = False
    air_timer = 0

    player_rect = pygame.Rect(100, 100, 5, 13)

    running = True
    while running:
        draw_text('Game', font, (0, 0, 0), screen, 20, 20)
        display.fill((255, 255, 255))
        
        tile_rects = []
        y = 0
        for layer in tiles:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(dirtImg,(x*16,y*16)) #16x16 is image resolution
                if tile == '2':
                    display.blit(grassImg,(x*16,y*16))
                if tile != '0':
                    tile_rects.append(pygame.Rect(x*16,y*16,16,16))
                x += 1
            y += 1

        player_movement = [0, 0]
        if moving_right == True:
            player_movement[0] += 3
        if moving_left == True:
            player_movement[0] -= 3
        player_movement[1] += vertical_momentum
        vertical_momentum += 0.2
        if vertical_momentum > 3:
            vertical_momentum = 3
        
        player_rect, collisions = move(player_rect, player_movement, tile_rects)

        if collisions['bottom'] == True:
            air_timer = 0
            vertical_momentum = 0
        else:
            air_timer += 1


        display.blit(playerImg, (player_rect.x, player_rect.y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_RIGHT:
                    moving_right = True
                if event.key == pygame.K_LEFT:
                    moving_left = True
                if event.key == pygame.K_SPACE:
                    if air_timer < 5:
                        vertical_momentum = -4
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    moving_right = False
                if event.key == pygame.K_LEFT:
                    moving_left = False

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0,0))
        pygame.display.update()
        clock.tick(60)

menu()


