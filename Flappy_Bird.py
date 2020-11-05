# <-- Flappy Bird Game using Pygame -->

# Importing Pygame and sys
import pygame as pg
import sys
import random

# Initializing Pygame
pg.init()
pg.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)

# Creating Screen
screen = pg.display.set_mode((288, 512))
clock = pg.time.Clock()

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
score_sound_countdown = 100

# Game Title and Icon
pg.display.set_caption('Flappy Bird')
icon = pg.image.load('favicon.png')
pg.display.set_icon(icon)

# Importing Images
# For Background
background_surface = pg.image.load('images/background-day.png').convert()

# For Floor
floor_surface = pg.image.load('images/base.png')
floor_x = 0

# For Bird
bird_surface = pg.image.load('images/bluebird-midflap.png').convert_alpha()
bird_rect = bird_surface.get_rect(center=(50, 256))

# For Pipes
pipe_surface = pg.image.load('images/pipe-green.png')
pipe_list = []
SPAWNPIPE = pg.USEREVENT
pg.time.set_timer(SPAWNPIPE, 1000)
pipe_height = [250, 300, 350, 400]

# Game over surface
game_over_surface = pg.image.load('images/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(144, 275))

# Adding Text (Score)
game_font = pg.font.Font('Font.ttf', 25)

# Importing Sounds
flap_sound = pg.mixer.Sound('audio/wing.wav')
death_sound = pg.mixer.Sound('audio/hit.wav')
score_sound = pg.mixer.Sound('audio/point.wav')


def draw_floor():
    screen.blit(floor_surface, (floor_x, 450))
    screen.blit(floor_surface, (floor_x + 288, 450))


def create_pipe():
    random_pipe = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(288, random_pipe))
    top_pipe = pipe_surface.get_rect(midbottom=(288, random_pipe - 150))
    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pg.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 450:
        death_sound.play()
        return False

    return True


def rotate_bird(bird):
    new_bird = pg.transform.rotozoom(bird, -bird_movement, 1)
    return new_bird


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render('Score : ' + str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render('Score : ' + str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render('High Score : ' + str(int(high_score)), True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(144, 50))
        screen.blit(high_score_surface, high_score_rect)


def update_high_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


# Starting Loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
                flap_sound.play()

            if event.key == pg.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, 256)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    # Background Surface and Floor
    screen.blit(background_surface, (0, 0))
    floor_x -= 1
    draw_floor()
    if floor_x <= -288:
        floor_x = 0

    if game_active:
        # Bird Movement
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Check Collision

        # Pipes
        pipe_list = move_pipe(pipe_list)
        draw_pipes(pipe_list)

        # Showing Score
        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_high_score(score, high_score)
        score_display('game_over')

    pg.display.update()

    clock.tick(60)
