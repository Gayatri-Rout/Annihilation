import random
import math
import pygame

# TO DO: fix disable shooting >>> game over


# mixer - class that handles music
from pygame import mixer

# colours used
white = (255, 255, 255)
black = (0, 0, 0)
light_purple = (255, 200, 255)

# screen.fill((0, 0, 0), [100, 285, 600, 30])  # screen.fill( colour, [width, height : position of rect,
# width, height: dimensions of rect]

# initialise pygame
pygame.init()

# create screen
screen_width = 800
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))  # width(x), height(y)

# title & icon
pygame.display.set_caption('ANNIHILATION')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# create start screen
start_text_font_1 = pygame.font.SysFont("Lucida sans typewriter regular", 50, 0, 0, None)  # says 'PROJECT ANNIHILATION'
start_text_font_2 = pygame.font.SysFont("CONSOLAS", 30, 0, 0, None)  # says 'PRESS 'P' TO PLAY'
start_text_font_3 = pygame.font.SysFont("CONSOLAS", 30, 0, 0, None)  # says 'PRESS 'S' FOR SETTINGS'
start_text_font_4 = pygame.font.SysFont("CONSOLAS", 30, 0, 0, None)  # says 'PRESS 'ESC' TO QUIT'

# player
playerimg = pygame.image.load('ship 128.png')
playerX = 355
playerY = 370
playerX_change = 0
playerY_change = 0

# creating multiple enemies using list
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 10

for i in range(no_of_enemies):
    enemyimg.append(pygame.image.load('enemy 64.png'))
    enemyX.append(random.randint(20, 720))
    enemyY.append(random.randint(20, 150))
    enemyX_change.append(5)
    enemyY_change.append(20)

# bullet
# ready - invisible bullet
# fire - visible & moving bullet
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 370
bulletY_change = 20
bullet_state = "ready"

# score
score = 0
scorex = 10
scorey = 10
score_font = pygame.font.SysFont("CONSOLAS", 30, 1)

# game over text
game_over_font = pygame.font.SysFont('CONSOLAS', 95, 10)
below_txt_font = pygame.font.SysFont('CONSOLAS', 28)


# any text to be displayed on screen;
def txt_text(font, txt, color, bg_colour):
    txt_surface = font.render(txt, True, color, bg_colour)
    return txt_surface, txt_surface.get_rect()


def txt_on_screen(font, txt, txt_w, txt_h, txt_color, txt_bg_color):
    txt_surf, txt_rect = txt_text(font, txt, txt_color, txt_bg_color)
    txt_rect.center = screen_width / 2 + txt_w, screen_height / 2 + txt_h
    screen.blit(txt_surf, txt_rect)


def start_screen():
    global running

    # background music for start screen
    mixer.music.load('start.mp3')
    mixer.music.play(-1)

    start = True
    while start:
        start_bg = pygame.image.load('start bg.PNG')
        screen.blit(start_bg, (0, 0))
        # centering 'PROJECT ANNIHILATION' (pa)
        txt_on_screen(start_text_font_1, "PROJECT ANNIHILATION", 0, (-100), white, black)

        # centering 'PRESS 'P' TO PLAY' (p)
        txt_on_screen(start_text_font_2, "Press 'p' to PLAY", 0, 0, black, light_purple)

        # centering 'PRESS 'S' FOR SETTINGS' (s)
        txt_on_screen(start_text_font_3, "Press 's' for SETTINGS", 0, 50, black, light_purple)

        # centering 'PRESS 'ESC' TO EXIT' (esc)
        txt_on_screen(start_text_font_4, "Press 'esc' to QUIT", 0, 100, black, light_purple)

        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                start, running = False

            if event1.type == pygame.KEYDOWN:
                if event1.key == pygame.K_p:
                    play = True
                    return play

                if event1.key == pygame.K_s:
                    start = False

                if event1.key == pygame.K_ESCAPE:
                    start = False

        pygame.display.update()


def display_score(x, y):
    # centering 'score' text using func: txt_on_screen
    txt_on_screen(score_font, "score: " + str(score), -320, -230, white, black)


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def game_over():
    global bullet_state
    # centering game-over text
    txt_on_screen(game_over_font, "GAME-OVER!", 0, 0, light_purple, None)
    # centering game-over 'instructions' text
    txt_on_screen(below_txt_font, "Press 'esc' to QUIT, 'enter' to RESTART", 0, 50, white, black)

    # game-over sound effect
    end_sound = mixer.Sound('end.wav')
    end_sound.play()
    mixer.music.set_volume(0)

    # disable shooting bullets
    for event2 in pygame.event.get():
        if event2.type == pygame.KEYDOWN:
            if event2.key == pygame.K_SPACE:
                bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 50, y + -45))


# bullet & enemy collision
def collision(a, b, c, d):
    distance = math.sqrt((math.pow(a - c, 2)) + (math.pow(b - d, 2)))
    if distance <= 26:
        return True
    else:
        return False


# enemy img changes to blast img
def enemy_to_blast(x, y):
    blast = pygame.image.load('blast 64.png')
    screen.blit(blast, (x, y))


# game loop
def game_loop():
    global playerX, playerY, playerX_change, playerY_change, bulletX, bulletY, bulletY_change, bullet_state
    global score, scorex, scorey

    # background music
    mixer.music.load('bg music.mp3')
    mixer.music.play(-1)

    running = True

    while running:

        # set background image(bg)
        bg = pygame.image.load('bg 2.PNG')
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            # movement of player L, R , U & D
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change -= 7

                if event.key == pygame.K_RIGHT:
                    playerX_change += 7

                if event.key == pygame.K_UP:
                    playerY_change -= 7

                if event.key == pygame.K_DOWN:
                    playerY_change += 7

                # update bullet position when shift in player position + bullet sound
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_sound = mixer.Sound('bullet.wav')
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0

        playerX += playerX_change
        # for player stay inside game window (L & R)
        if playerX >= 650:  # R
            playerX = 650
        elif playerX <= 20:  # L
            playerX = 20

        playerY += playerY_change
        # for player stay inside game window (U & D)
        if playerY >= 370:  # D
            playerY = 370
        if playerY <= 350:  # U
            playerY = 350

        # for enemies to stay inside game window & enemies movement
        for i in range(no_of_enemies):
            # game over
            if enemyY[i] >= 340:
                for j in range(no_of_enemies):
                    enemyY[j] = 1000
                game_over()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] >= 720:  # R
                enemyX_change[i] -= 5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] <= 20:  # L
                enemyX_change[i] += 5
                enemyY[i] += enemyY_change[i]

            # collision for every enemy
            result = collision(enemyX[i], enemyY[i], bulletX, bulletY)
            if result:
                enemy_to_blast(enemyX[i], enemyY[i])
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                score += 1
                bulletY = 445
                bullet_state = "ready"
                enemyX[i] = random.randint(20, 720)
                enemyY[i] = random.randint(20, 150)

            # call enemy func
            enemy(enemyX[i], enemyY[i], i)

        # bullet movement
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
            # re-appearance of bullet at start point
            if bulletY <= 0:  # U
                bulletY = 445
                bullet_state = "ready"

        # call funcs 'player' & 'score'
        player(playerX, playerY)
        display_score(scorex, scorey)

        pygame.display.update()


start_screen()
game_loop()

pygame.display.update()

