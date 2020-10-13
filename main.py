import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()

# making screen of game
screen = pygame.display.set_mode((800, 600))

# Setting logo icon and title
pygame.display.set_caption("SpaceInvaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# editing background for the game
background = pygame.image.load(
    "backgroundedited_800x600.jpg")
# Background sound
mixer.music.load("bgmusic.mp3")
mixer.music.play(-1)

# Putting player image and setting properties
Playerimg = pygame.image.load("player.png")
PlayerX = 370
PlayerY = 480
PlayerX_change = 0
PlayerY_change = 0


def setplayer(x, y):
    screen.blit(Playerimg, (x, y))


# Setting Enemy image and properties
def setenemy(x, y, i):
    screen.blit(Enemyimg[i], (x, y))


# Creating List

Enemyimg = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
numofenemies = 20
count = numofenemies // 2
for i in range(count):
    Enemyimg.append(pygame.image.load("redenemy.ico"))
    EnemyX.append(random.randint(0, 735))
    EnemyY.append(random.randint(50, 150))
    Enemyimg.append(pygame.image.load("whiteenemy.ico"))
    EnemyX.append(random.randint(0, 735))
    EnemyY.append(random.randint(50, 150))
    EnemyX_change.append(3)
    EnemyY_change.append(40)


def setenemy(x, y, i):
    screen.blit(Enemyimg[i], (x, y))


# Setting Bullet image and initial properties
Bulletimg = pygame.image.load("bullet.png")
BulletX = PlayerX
BulletY = 480
BulletX_change = 0
BulletY_change = 10
Bullet_Status = "ready"


def FireBullet(x, y):
    global Bullet_Status
    Bullet_Status = "fire"
    screen.blit(Bulletimg, (x, y))


# making score system
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10


def show_score(textX, textY):
    score = font.render("Socre : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (textX, textY))


def isCollision(EnemyX, EnemyY, BulletX, BulletY):
    distance = math.sqrt(
        (math.pow(EnemyX - BulletX, 2) + math.pow(EnemyY - BulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Over Font

gameoverfont = pygame.font.Font("freesansbold.ttf", 64)


# Game over function
def gameover():
    overtext = gameoverfont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(overtext, (200, 250))


# Game Lopp
running = True
while running:
    # Screen fill with red,blue green
    screen.fill((0, 0, 0))

    # Screen Background setting
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PlayerX_change = -5
            if event.key == pygame.K_RIGHT:
                PlayerX_change = 5
            if event.key == pygame.K_SPACE:
                if Bullet_Status is "ready":
                    BulletX = PlayerX
                    FireBullet(BulletX + 16, BulletY + 10)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PlayerX_change = 0
    # Chaging player value to move
    PlayerX += PlayerX_change

    # Checking boundaries for player
    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX > 736:
        PlayerX = 736
    for i in range(numofenemies // 2):
        # Is gameover
        if EnemyY[i] > 440:
            for j in range(numofenemies):
                EnemyY[j] = 2000
                gameover()
            break
        # Enemy Movement
        EnemyX[i] += EnemyX_change[i]
        # checking boundaries for enemy
        if EnemyX[i] <= 0:
            EnemyX_change[i] = 3
            EnemyY[i] += EnemyY_change[i]
        elif EnemyX[i] > 736:
            EnemyX_change[i] = -3
            EnemyY[i] += EnemyY_change[i]
        # Checking collision between enemy and bullet
        collision = isCollision(EnemyX[i], EnemyY[i], BulletX, BulletY)
        if collision:
            collisionsound = mixer.Sound("explosion.wav")
            collisionsound.play()
            score_value += 1
            BulletY = 480
            Bullet_Status = "ready"
            EnemyX[i] = random.randint(0, 735)
            EnemyY[i] = random.randint(50, 150)
        setenemy(EnemyX[i], EnemyY[i], i)
    # Checking if bullet is in the screen to fire again or not
    if BulletY <= 0:
        BulletY = 480
        Bullet_Status = "ready"

    # Checking Bullet fire condition
    if Bullet_Status is "fire":
        bulletsound = mixer.Sound("pew.wav")
        bulletsound.play()
        FireBullet(BulletX + 16, BulletY + 10)
        BulletY -= BulletY_change

    # Showing enemies and player on the screen
    setplayer(PlayerX, PlayerY)

    # Showing score
    show_score(textX, textY)

    # Updating the screen
    pygame.display.update()
