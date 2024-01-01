import pygame
from pygame.locals import *
import random
import os

pygame.init()

#Fenetre
screen_height = 500
screen_width = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake')
background = pygame.image.load("image/Gameboy.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

#Variables
black="#000000"
white="#ffffff"
green="#9BBA5B"
red="#c41818"
gameboy_area = pygame.Rect(200, 100, 400, 300)
segment_size=20
snake = [pygame.Rect(300, 300, segment_size, segment_size)]
snake_dir=(0,0)
time, time_step = 0,130
clock=pygame.time.Clock()
current_direction = "RIGHT"
segments_to_add = 1
first_collision = True
retro_path = os.path.join("font", "RetroGaming.ttf")
retro_font = pygame.font.Font(retro_path, 30)
retro_font2 = pygame.font.Font(retro_path, 20)
white="#ffffff"
score = 0


#Fonctions
def draw_grid(surface,area,cell_size,color):
    for x in range(area.left, area.right, cell_size):
        pygame.draw.line(surface, color, (x, area.top), (x, area.bottom))

    for y in range(area.top, area.bottom, cell_size):
        pygame.draw.line(surface, color, (area.left, y), (area.right, y))

def draw_snake():
    global segments_to_add

    for segment in snake:
        pygame.draw.rect(screen, black, segment)

def check_collision():
    global segments_to_add, apple, first_collision, score

    if snake[0].colliderect(apple):
        if first_collision:
            segments_to_add = 2 
            first_collision = False
        else :
            segments_to_add = 1 
            apple = generate_apple()
            score += 1

        last_segment = snake[-1]
        new_segment = pygame.Rect(last_segment.x, last_segment.y, segment_size, segment_size)
        snake.append(new_segment)

def check_self_collision():
    head = snake[0]
    for segment in snake[3:]:
        if head.colliderect(segment):
            return True
    return False

def generate_apple():
    apple_x = random.randint(gameboy_area.left // segment_size, (gameboy_area.right - segment_size) // segment_size) * segment_size
    apple_y = random.randint(gameboy_area.top // segment_size, (gameboy_area.bottom - segment_size) // segment_size) * segment_size
    return pygame.Rect(apple_x, apple_y, segment_size, segment_size)
    
apple = generate_apple()

def reset_game():
    global snake, snake_dir, segments_to_add, first_collision, apple, game_over,score
    min_x = gameboy_area.left // segment_size
    max_x = (gameboy_area.right - segment_size) // segment_size
    min_y = gameboy_area.top // segment_size
    max_y = (gameboy_area.bottom - segment_size) // segment_size

    snake_x = random.randint(min_x, max_x) * segment_size
    snake_y = random.randint(min_y, max_y) * segment_size
    snake = [pygame.Rect(snake_x, snake_y, segment_size, segment_size)]
    
    score=0
    snake_dir = (0, 0)
    segments_to_add = 1
    first_collision = True
    apple = generate_apple()
    game_over = False




#Run les events et le jeu
run = True
game_over = False


while run:

    screen.fill(white)
    screen.blit(background, (0,0))
    pygame.draw.rect(screen, green, gameboy_area)
    pygame.draw.rect(screen, red, apple)
    draw_grid(screen, gameboy_area, 20, black)

    check_collision()
    draw_snake()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if game_over == False:
                if event.key == pygame.K_UP and current_direction != "DOWN":
                    snake_dir = (0, -segment_size)
                    current_direction = "UP"
                if event.key == pygame.K_DOWN and current_direction != "UP":
                    snake_dir = (0, segment_size)
                    current_direction = "DOWN"
                if event.key == pygame.K_LEFT and current_direction != "RIGHT":
                    snake_dir = (-segment_size, 0)
                    current_direction = "LEFT"
                if event.key == pygame.K_RIGHT and current_direction != "LEFT":
                    snake_dir = (segment_size, 0)
                    current_direction = "RIGHT"
            else :
                if event.key == pygame.K_r:
                    reset_game()

    if snake[0].left < gameboy_area.left + segment_size and snake_dir == (-segment_size, 0):
        snake_dir = (0, snake_dir[1])
        game_over = True
    elif snake[0].right > gameboy_area.right - segment_size and snake_dir == (segment_size, 0):
        snake_dir = (0, snake_dir[1])
        game_over = True
    elif snake[0].top < gameboy_area.top + segment_size and snake_dir == (0, -segment_size):
        snake_dir = (snake_dir[0], 0)
        game_over = True
    elif snake[0].bottom > gameboy_area.bottom - segment_size and snake_dir == (0, segment_size):
        snake_dir = (snake_dir[0], 0)
        game_over = True

    if check_self_collision():
        game_over = True
        
    if game_over:
        loss_text = retro_font.render('Vous avez perdu !', True, white)
        loss2_text = retro_font2.render('Appuyez sur "R" pour rejouer', True, white)
        screen.blit(loss_text, (screen_width // 2 - 168, screen_height // 2 - 25))
        screen.blit(loss2_text, (screen_width // 2 - 195, screen_height // 2 + 10))

    time_now = pygame.time.get_ticks()

    if time_now - time > time_step and snake_dir != (0, 0):
        time = time_now
        snake[0].move_ip(snake_dir)
        for i in range(len(snake) - 1, 0, -1):
            snake[i].x = snake[i - 1].x
            snake[i].y = snake[i - 1].y

    score_text = retro_font.render(f'Score: {score}', True, white)
    screen.blit(score_text, (320, 63))

    clock.tick(120)
    pygame.display.update()

pygame.quit()