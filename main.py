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
icon = pygame.image.load('player.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('player.png').convert()
playerImg.set_colorkey((255, 255, 255))

#Tiles
grassImg = pygame.image.load('grass.png')
dirtImg = pygame.image.load('dirt.png')

def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()

    data = data.split('\n')
    tiles = []
    for row in data:
        tiles.append(list(row))

    return tiles

tiles = load_map('map')

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

        button_1 = pygame.Rect(50, 100, 50, 25)

        if button_1.collidepoint((mx, my)):
            if click:
                game()

        pygame.draw.rect(screen, (255, 0, 0), button_1)

        draw_text('Play', font, (0, 0, 0), screen, 50, 100)

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
        clock.tick(60)

def game():
    vertical_momentum = 0
    moving_right = False
    moving_left = False
    air_timer = 0
    true_scroll = [0,0]

    player_rect = pygame.Rect(100, 100, 5, 13)

    #Background objects for paralax scrolling, [X, Y, Width, Height]
    background_objects = [[0.12, [80, 5, 90, 400]], [0.25, [120, 10, 70, 400]], [0.25, [120, 10, 70, 400]], [0.25, [280, 30, 40, 400]], [0.5, [30, 40, 40, 400]], [0.5, [130, 90, 100, 400]], [0.5, [300, 80, 120, 400]]]

    running = True
    while running:
        display.fill((126, 19, 158))

        #Screen scroll, following character
        true_scroll[0] += (player_rect.x - true_scroll[0] - 152) / 20 #-152 / -106 to correctly display with chosen display size
        true_scroll[1] += (player_rect.y - true_scroll[1] - 106) / 20 #/20 makes camera smoother
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        #Background object paralax scrolling, line 148
        pygame.draw.rect(display, (59, 0, 77), pygame.Rect(0, 120, 300, 800))
        for background_object in background_objects:
            obj_rect = pygame.Rect(background_object[1][0] - scroll[0] * background_object[0], #x-axis
                       background_object[1][1] - scroll[1] * background_object[0], #y-axis
                       background_object[1][2], #width
                       background_object[1][3]) #height
            if background_object[0] == 0.5:
                pygame.draw.rect(display, (77, 0, 64), obj_rect)
            elif background_object[0] == 0.25:
                pygame.draw.rect(display, (156, 0, 134), obj_rect)
            else:
                pygame.draw.rect(display, (255, 0, 212), obj_rect)
        

        #Generate tiles based on map.txt
        tile_rects = []
        y = 0
        for layer in tiles:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(dirtImg,(x*16 - scroll[0], y*16 - scroll[1])) #16x16 is image resolution
                if tile == '2':
                    display.blit(grassImg,(x*16 - scroll[0], y*16 - scroll[1]))
                if tile != '0':
                    tile_rects.append(pygame.Rect(x*16, y*16, 16, 16))
                x += 1
            y += 1

        #Basic player movement physics
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

        #Stops character from performing infinite mid-air jumps
        if collisions['bottom'] == True:
            air_timer = 0
            vertical_momentum = 0
        else:
            air_timer += 1

        #Character display
        display.blit(playerImg, (player_rect.x - scroll[0], player_rect.y - scroll[1]))

        #Keyboard controls
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
                        vertical_momentum = -4 #Effects height of jump
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    moving_right = False
                if event.key == pygame.K_LEFT:
                    moving_left = False

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0,0))
        draw_text('Game', font, (0, 0, 0), screen, 20, 20)
        pygame.display.update()
        
        #Locks FPS at 60 
        #NOTE: The higher the FPS the higher the speed of the game
        clock.tick(60)

menu()


