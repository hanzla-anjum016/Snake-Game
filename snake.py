import pygame
import random
import os
from pygame import *

pygame.mixer.init()
pygame.init()

# Colors 
gold = (255,215,0)
black = (0,0,0)
red = (255,0,0)
silver = (192,192,192)
violet = (238,130,238)
pink = (255,192,203)
chocolate = (210,105,30)
snow = (255,250,250)
white = (255,255,255)

# Creating window
screen_width = 1000
screen_height = 670
gameWindow = pygame.display.set_mode((screen_width, screen_height))


# creating background
bgimg = pygame.image.load('asset\\bg2.jpg')
bgimg= pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

overimg = pygame.image.load('asset\\outro2.png')
overimg = pygame.transform.scale(overimg, (screen_width, screen_height)).convert_alpha()

welcome_img = pygame.image.load('asset\\Intro-h.png')
welcome_img = pygame.transform.scale(welcome_img, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("Snake game")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    fps = 30
    pygame.mixer.music.load('asset\\wc.mp3')
    pygame.mixer.music.play()
    while not exit_game:
        gameWindow.blit(welcome_img, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.load('asset\\bgm.mp3')
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(fps)


# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    snk_color = red
    food_color = gold

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(100, screen_height / 2)
    score = 0
    init_velocity = 6
    snake_size = 10
    fps = 30

    # check if highscore.txt exists
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")
            
    with open("highscore.txt", "r") as f:
        highscore = f.read()
    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as w:
                w.write(str(highscore))
            gameWindow.blit(overimg, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        score += 10

                    if event.key == pygame.K_o:
                        game_over = True

                    if event.key == pygame.K_r:
                        if init_velocity != 30:
                            init_velocity += 1

                    if event.key == pygame.K_d:
                        if init_velocity != 1:
                            init_velocity -= 1
                        
                    if event.key == pygame.K_c:        
                        if snk_color == red:
                            snk_color = black
                            food_color = gold
                        elif snk_color == black:
                            snk_color = gold
                            food_color = black
                        elif snk_color == gold:
                            snk_color = silver
                            food_color = violet
                        elif snk_color == silver:
                            snk_color = violet
                            food_color = silver
                        elif snk_color == violet:
                            snk_color = snow
                            food_color = chocolate
                        elif snk_color == snow:
                            snk_color = white
                            food_color = silver
                        elif snk_color == white:
                            snk_color = chocolate
                            food_color = snow
                        elif snk_color == chocolate:
                            snk_color = pink
                            food_color = violet
                        elif snk_color == pink:
                            snk_color = red
                            food_color = black
                            
                    if event.key == pygame.K_l:
                        snk_length += 1

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<10 and abs(snake_y - food_y)<10:
                score +=10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 3
                if score>int(highscore):
                    highscore = score

            gameWindow.blit(bgimg, (0, 0))
            text_screen(" HighScore: " + str(highscore), black, 700, 10)
            text_screen("Speed: " + str(init_velocity), black, 10, 10)
            text_screen("Score: " + str(score), black, 415, 10)
            pygame.draw.circle(gameWindow, food_color, [food_x, food_y], 7)


            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('asset\\bgm1.mp3')
                pygame.mixer.music.play() 

            if snake_x<7 or snake_x>screen_width or snake_y<7 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('asset\\bgm1.mp3')
                pygame.mixer.music.play()
            plot_snake(gameWindow, snk_color, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()