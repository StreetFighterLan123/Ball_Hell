import pygame
import time
import os
import sys
import random
import math

# For FPS

clock = pygame.time.Clock()


def colorize(image, newColor):
    """
    Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
    original).
    :param image: Surface to create a colorized copy of
    :param newColor: RGB color to use (original alpha values are preserved)
    :return: New colorized Surface instance
    """
    image = image.copy()

    # zero out RGB values
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    # add in new RGB values
    image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

    return image


# Line for end game thing.
def line(x):
    for x in range(0, x):
        print("                                ")


pygame.init()
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('hell.png')

pygame.display.set_caption("Ball Hell")
pygame.display.set_icon(pygame.image.load('hell.png'))

# Character
orig_Img = pygame.image.load('player.png')
orig_Img = colorize(orig_Img, (255, 192, 203))
playerImg = pygame.transform.scale(orig_Img, (30, 30))
playerX = 380
playerY = 530
playerX_vel = 0
playerY_vel = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Balls

ballImg = []
ballX = []
ballY = []
ballY_vel = []
num_of_balls = 10


def ball_thing():
    for i in range(num_of_balls):
        ballImg.append(pygame.image.load('ball.png'))
        ballX.append(random.randint(0, 775))
        ballY.append(20)
        ballY_vel.append(10)


ball_thing()


def ball(x, y, i):
    screen.blit(ballImg[i], (x, y))


# Collision Function


# Score Function
score = 0

font = pygame.font.Font('freesansbold.ttf', 32)


def score_disp():
    score_text = font.render((f'Score: {round(score)}'), True, (255, 192, 203))
    screen.blit(score_text, (355, 50))


# Fix this later! Use the bad one I wrote before for now...or forever...
def is_collided_with(sprite_one, sprite_two):
    return sprite_one.rect.colliderect(sprite_two.rect)


pygame.mixer.music.load("adventure.wav")
pygame.mixer.music.play(-1)

running = True

x_vel_base = 25
while running:
    playerX_vel = 0
    playerY_vel = 0
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

    # For the player movement that's going to happen later on.
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        playerX_vel = x_vel_base

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        playerX_vel = -x_vel_base

    playerX -= playerX_vel
    playerY -= playerY_vel

    for i in range(num_of_balls):
        ballY[i] += ballY_vel[i]
        ball(ballX[i], ballY[i], i)
        # if collision:
        #    running = False
        #    sys.exit()
        if ballY[i] > 660:
            ball_thing()
            ballY[i] = 10
            ballX[i] = random.randint(0, 775)
            ballY_vel[i] += 0.25
            score += 0.1
        if abs(ballX[i] - playerX) < 15 and abs(ballY[i] - playerY) < 70:
            running = False
            line(10)
            print(f'Your score was: {round(score)}')
            break
            sys.exit()
    if playerX < 0:
        playerX = 0
    if playerX > 738:
        playerX = 738

    score_disp()
    player(playerX, playerY)
    clock.tick(30)
    # print(playerX) for development
    pygame.display.update()
