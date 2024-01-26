#importing modules
import pygame
import random
import os

#initializing commands
pygame.init()
pygame.mixer.init()

# color
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green=(0,255,0)
grey=(220,220,220)


# height and width of display
screen_width = 900
screen_height = 600

#loading screen images
screen1=pygame.image.load("snake3.png")
screen2=pygame.image.load("screen2.png")
bgimg=pygame.image.load("snake1.jpg")
bgimg=pygame.transform.scale(bgimg,(screen_width,screen_height))

# creating window
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# creating title
pygame.display.set_caption("Snake Game By Hashir Soomro")
pygame.display.update()

#direction and snake starting image
direction="right"
snakeHeadImg = pygame.image.load("snakeimg.png")

# using clock and font selection func
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 33)

#defining functions
def screen_score(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake( gameWindow , snake_list, snake_size):
    if direction == "right":
        s_head = pygame.transform.rotate(snakeHeadImg,270)

    elif direction == "left":
        s_head = pygame.transform.rotate(snakeHeadImg, 90)

    elif direction == "up":
        s_head = snakeHeadImg

    elif direction == "down":
        s_head = pygame.transform.rotate(snakeHeadImg, 180)

    gameWindow.blit(s_head, (snake_list[-1][0], snake_list[-1][1]))
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, green, [x, y, snake_size, snake_size])

def welcome():
    exit_game=False
    while not exit_game:
        gameWindow.fill(white)
        gameWindow.blit(screen1,[0,0])
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                exit_game=True
            if event.type== pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    gameLoop()
            pygame.display.update()
            clock.tick(40)
# game loop
def gameLoop():
    # game specific variable
    global direction

    exit_game = False
    game_over = False
    snake_x = screen_width/2
    snake_y = screen_height/2
    snake_size = 10
    fps = 40
    velocity_x = 0
    velocity_y = 0
    #food_x = random.randint(25, screen_width / 1.25)
    food_x = random.randint(25, int(screen_width / 1.25))

    #food_y = random.randint(25, screen_height / 1.25)
    food_y = random.randint(25, int(screen_height / 1.25))

    score = 0
    init_velocity = 5
    snake_list = []
    snake_length = 1
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt","w") as f:
            f.write("0")
    with open("highscore.txt", "r")as f:
        highscore = f.read()

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w")as f:
                f.write(str(highscore))
            gameWindow.fill(black)
            gameWindow.blit(screen2, [0, 0])
            screen_score(f"{score}", white, 470, 388)
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
                    if (event.key == pygame.K_LEFT) and direction != "right":
                        velocity_x = -init_velocity
                        velocity_y = 0
                        direction = "left"

                    if (event.key == pygame.K_RIGHT) and direction != "left":
                        velocity_x = init_velocity
                        velocity_y = 0
                        direction = "right"

                    if (event.key == pygame.K_DOWN) and direction != "up":
                        velocity_y = init_velocity
                        velocity_x = 0
                        direction = "down"

                    if (event.key == pygame.K_UP) and direction != "down":
                        velocity_y = -init_velocity
                        velocity_x = 0
                        direction = "up"

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y
            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                score += 10
                #food_x = random.randint(30, screen_width / 1.25)
                food_x = random.randint(30, int(screen_width / 1.25))
                
                #food_y = random.randint(30, screen_height / 1.25)
                food_y = random.randint(30, int(screen_height / 1.25))

                snake_length += 3
                if score > int(highscore):
                    highscore = score

            gameWindow.fill(black)
            gameWindow.blit(bgimg,(0,0))
            screen_score("score:" + str(score) + "   Hiscore:" + str(highscore),grey, 5, 5)
            pygame.draw.circle(gameWindow, red, [food_x, food_y], 6, 6)
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]
            if head in snake_list[:-1]:
                pygame.mixer.music.load("explosion.mp3")
                pygame.mixer.music.play()
                game_over = True
            if snake_x > screen_width or snake_x < 0 or snake_y > screen_height or snake_y < 0:
                pygame.mixer.music.load("explosion.mp3")
                pygame.mixer.music.play()
                game_over = True
            plot_snake(gameWindow,snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()

welcome()
