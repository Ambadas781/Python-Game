import random
import math
import pygame
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background2.png')
mixer.music.load('jailer.mpeg')
mixer.music.play(-1)
pygame.display.set_caption("Space Battle")
icon = pygame.image.load('space.png')
pygame.display.set_icon(icon)
playerImg = pygame.image.load('space.png')
playerX = 370
playerY = 480
playerX_change = 0
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_of_aliens = 6
for i in range(num_of_aliens):
    alienImg.append(pygame.image.load('alien.png'))
    alienX.append(random.randint(0, 736))
    alienY.append(random.randint(50, 150))
    alienX_change.append(4)
    alienY_change.append(40)

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('SPACE.ttf', 30)
textX = 10
textY = 10
game_over = pygame.font.Font('SPACE.ttf', 40)



def show_score(x, y):
    score = font.render("score : " + str(score_value), True, (255, 140, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = game_over.render("GAME OVER " , True, (255, 140, 0))
    screen.blit(over_text, (196, 236))




def player(x, y):
    screen.blit(playerImg, (x, y))


def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt(math.pow(alienX - bulletX, 2) + (math.pow(alienY - bulletY, 2)))
    if distance < 20:
        return True
    else:
        return False


running = True
while running:
    # rgb(red,green,blue)
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change = -2.6
            if event.key == pygame.K_RIGHT:
                playerX_change = 2.6
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('back.mp3')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    for i in range(num_of_aliens):
        if alienY[i] > 428:
            for j in range(num_of_aliens):
                alienY[j] = 2000
            game_over_text()
            break
        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] = 2.6
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -2.6
            alienY[i] += alienY_change[i]

        collision = isCollision(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('sound.mpeg')
            explosion_sound.play()

            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            alienX[i] = random.randint(0, 736)
            alienY[i] = random.randint(50, 150)
        alien(alienX[i], alienY[i], i)
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
