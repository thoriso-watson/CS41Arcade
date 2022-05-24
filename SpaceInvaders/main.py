import pygame
import random
import math
from pygame import mixer

# INITIALIZE PYGAME
pygame.init()

# CREATE SCREEN
WIDTH, HEIGHT = 700, 800
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )

# BACKGROUND
background = pygame.image.load('space.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
rect = background.get_rect()
rect = rect.move((0,0))

# BACKGROUND SOUND
mixer.music.load('background.wav')
mixer.music.play(-1) # -1 play on loop

# TITLE AND ICON
pygame.display.set_caption("Space Invaders")
ICON = pygame.image.load('spaceship.png')
pygame.display.set_icon(ICON)

# PLAYER
PLAYER_IMG = pygame.image.load('player.png')
playerX = (1/2) * WIDTH - 30 # player_IMG is 60x60px
playerY = 670
playerX_vel = 0
playerY_vel = 0

# ENEMY
enemy_images = ['enemy1.png', 'enemy2.png']
ENEMY_IMG = []
enemyX = []
enemyY = []
enemyX_vel = []
enemyY_vel = []
num_enemy = 5
for i in range(num_enemy):
    ENEMY_IMG.append(pygame.image.load(random.choice(enemy_images)))
    enemyX.append(random.randint(100, WIDTH - 160))
    enemyY.append(random.randint(-150, 150))
    enemyX_vel.append(random.choice([-2, 2]))
    enemyY_vel.append(.8)

# PLAYER BULLET
BULLET_IMG = pygame.image.load('bullet.png')
bulletX = playerX
bulletY = playerY
bulletY_vel = -20
bullet_state = 'ready' # ready state: can't see the bullet on screen; # fire state: bullet is moving and visible

# ENEMY BULLET
ENEMY_BULLET_IMG = pygame.image.load('enemy_bullet.png')
ENEMY_BULLET_IMG = pygame.transform.rotate(ENEMY_BULLET_IMG, 270)
enemy_bulletX = enemyX
enemy_bulletY = enemyY
enemy_bulletY_vel = 2

# SCORE + WAVE TEXT
score_value = 0
wave_value = 1
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# GAME OVER TEXT
over_font = pygame.font.Font('freesansbold.ttf', 64)

# PLAYER, ENEMY, BULLET, COLLISION, TEXT FUNCTIONS
def player(x, y):
    screen.blit(PLAYER_IMG, (x, y))

def enemy(x, y, i):
    screen.blit(ENEMY_IMG[i], (x,y))

def fireBullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(BULLET_IMG, (x - 10, y - 10))

def fireEnemyBullet(x, y):
    screen.blit(ENEMY_BULLET_IMG, (x, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX + 30) - bulletX, 2) + math.pow((enemyY + 30) - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

def showScore(x, y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def gameOver():
    over = over_font.render("GAME OVER", True, (255,255,255))
    score_over = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(over, [.5 * WIDTH - 200, .5 * HEIGHT - 64])
    screen.blit(score_over, [.5 * WIDTH - 200, .5 * HEIGHT])

# GAME LOOP
running = True
while running:
    # SCREEN
    screen.blit(background, rect)
    # PYGAME EVENTS
    for event in pygame.event.get():
        # QUIT
        if event.type == pygame.QUIT:
            running = False
        # MOVEMENT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_vel = -6
            if event.key == pygame.K_d:
                playerX_vel = 6
            if event.key == pygame.K_w:
                playerY_vel = -4
            if event.key == pygame.K_s:
                playerY_vel = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fireBullet(playerX, playerY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_vel = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                playerY_vel = 0
    # PLAYER MOVEMENT
    playerX += playerX_vel
    playerY += playerY_vel
    # PLAYER BOUNDARIES
    if playerX <= 0:
        playerX = 0
    elif playerX >= WIDTH - 65:
        playerX = WIDTH - 65
    if playerY <= 0:
        playerY = 0
    elif playerY >= HEIGHT - 65:
        playerY = HEIGHT - 65
    # ENEMY MOVEMENT
    for i in range(num_enemy):
        # GAME OVER
        if enemyY[i] > (HEIGHT - 60):
            for j in range(num_enemy):
                enemyY[i] = 2000
            gameOver()
            break
        # ENEMY MOVE
        enemyX[i] += enemyX_vel[i]
        enemyY[i] += enemyY_vel[i]
        # ENEMY BOUNDARIES
        if enemyX[i] <= 0:
            enemyX_vel[i] = 2
        elif enemyX[i] >= WIDTH - 65:
            enemyX_vel[i] = -2
        # COLLISION
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision == True:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletX = playerX
            bulletY = playerY
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(100, WIDTH - 160)
            enemyY[i] = random.randint(10, 150)
        # ENEMY BLIT FUNCTION
        enemy(enemyX[i], enemyY[i], i)
    # BULLET MOVEMENT
    if bullet_state == 'fire':
        fireBullet(bulletX, bulletY)
        bulletY += bulletY_vel
    if bulletY <= 0:
        bullet_state = 'ready'
    # # ENEMY BULLET MOVEMENT
    # fireEnemyBullet(enemy_bulletX, enemy_bulletY)
    # enemy_bulletY += enemy_bulletY_vel
    # if enemy_bulletY > HEIGHT:
    #     enemy_bulletX = enemyX
    #     enemy_bulletY = enemyY

    # PLAYER FUNCTION
    player(playerX, playerY)

    # SCORE
    showScore(textX, textY)

    # UPDATE DISPLAY
    pygame.display.update() # Updates the screen.


    # NEXT GAME:
        # Add enemy bullets.
        # Add player health.
        # Add cooldown timer.
        # Add waves and levels.
