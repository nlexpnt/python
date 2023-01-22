import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
from random import randint
from os import listdir
import os

pygame.init()

FPS = pygame.time.Clock()

screen = width, height = 800, 600

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
IMGS_PATH = 'goose'

font = pygame.font.SysFont('Verdana', 20)

main_surface = pygame.display.set_mode(screen)
s = 'sound'
bg_sound = pygame.mixer.music.load(os.path.join(s, 'fon.ogg'))
bonus_sound = pygame.mixer.Sound(os.path.join(s, 'bonus.ogg'))
crash_sound = pygame.mixer.Sound(os.path.join(s, 'crash.ogg'))
pygame.mixer.music.play(-1)


def random_color():
    color = randint(150, 200), randint(0, 250), randint(100, 200)
    return color


player_imgs = [pygame.transform.scale(pygame.image.load(
    IMGS_PATH + '/' + file).convert_alpha(), (100, 50)) for file in listdir(IMGS_PATH)]
player = player_imgs[0]
player_rect = player.get_rect()
player_speed = 4


def create_enemy():
    enemy = pygame.transform.scale(pygame.image.load(
        'enemy.png').convert_alpha(), (90, 30))
    enemy_rect = pygame.Rect(width, randint(30, height-30), *enemy.get_size())
    enemy_speed = randint(4, 6)
    return [enemy, enemy_rect, enemy_speed]


def create_bonus():
    bonus = pygame.transform.scale(pygame.image.load(
        'bonus.png').convert_alpha(), (100, 150))
    bonus_rect = pygame.Rect(randint(50, width - 100), 0, *bonus.get_size())
    bonus_speed = randint(1, 3)
    return [bonus, bonus_rect, bonus_speed]


bg = pygame.transform.scale(pygame.image.load(
    'background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 2

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, randint(1000, 1500))

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, randint(1000, 2000))

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

img_index = 0
scores = 0
lives = 3
enemies = []
bonuses = []


is_working = True

while is_working:

    FPS.tick(90)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]

    pressed_keys = pygame.key.get_pressed()

    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < -bg.get_width():
        bgX = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))

    main_surface.blit(player, player_rect)
    main_surface.blit(font.render('Score: ' + str(scores), True, GREEN), (width - 100, 0))
    main_surface.blit(font.render('Live: ' + str(lives), True, RED), (20, 0))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
            enemies.pop(enemies.index(enemy))
            pygame.mixer.Sound.play(crash_sound)
            lives -= 1
            if lives <= 0:
                is_working = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom >= height:
            bonuses.pop(bonuses.index(bonus))

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            pygame.mixer.Sound.play(bonus_sound)
            scores += 1

    if pressed_keys[K_DOWN] and not player_rect.bottom >= height:
        player_rect = player_rect.move((0, player_speed))
    if pressed_keys[K_UP] and not player_rect.top < 0:
        player_rect = player_rect.move((0, -player_speed))
    if pressed_keys[K_LEFT] and not player_rect.left < 0:
        player_rect = player_rect.move((-player_speed, 0))
    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move((player_speed, 0))

    pygame.display.flip()
