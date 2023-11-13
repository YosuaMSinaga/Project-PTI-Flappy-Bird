# Import library
import pygame
import sys
import time
import random
from pygame import mixer

# analisis pygame
pygame.init()

# Frame per detik
clock = pygame.time.Clock()

# Deklarasi sound Efect
music=pygame.mixer.music.load('C:\\Users\\Reaper\Music\\audio2.wav')
score_sound =pygame.mixer.Sound('C:\\Users\Reaper\\Music\\audio1.wav')
lompat_sound=pygame.mixer.Sound('C:\\Users\\Reaper\\Music\\audio3.wav')

# Function untuk gambar
def draw_floor():
    screen.blit(floor_img, (floor_x, 520))
    screen.blit(floor_img, (floor_x + 448, 520))

# Function untuk membuat pipa
def create_pipes():
    pipe_y = random.choice(pipe_height)
    top_pipe = pipe_img.get_rect(midbottom=(467, pipe_y - 300))
    bottom_pipe = pipe_img.get_rect(midtop=(467, pipe_y))
    return top_pipe, bottom_pipe

# Function untuk animasi
def pipe_animation():
    global game_over, score_time
    for pipe in pipes:
        if pipe.top < 0:
            flipped_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flipped_pipe, pipe)
        else:
            screen.blit(pipe_img, pipe)

        pipe.centerx -= 3
        if pipe.right < 0:
            pipes.remove(pipe)

        if bird_rect.colliderect(pipe):
            game_over = True
# Game window
width, height = 350, 622
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

# Pengaturan background dan base image
back_img = pygame.image.load("C:\\Users\\Reaper\\Documents\\ASET GAME DEVPY\\Aset Objek\\background.png")
floor_img = pygame.image.load("C:\\Users\\Reaper\\Documents\\ASET GAME DEVPY\\Aset Objek\\Tanah.png")
floor_x = 0

# different stages of bird
bird_up = pygame.image.load("C:\\Users\\Reaper\\Documents\\ASET GAME DEVPY\\Aset Objek\\B.png")
bird_down = pygame.image.load("C:\\Users\\Reaper\\Documents\\ASET GAME DEVPY\\Aset Objek\\B1.png")
bird_mid = pygame.image.load("C:\\Users\\Reaper\\Documents\\ASET GAME DEVPY\\Aset Objek\\B2.png")
birds = [bird_up, bird_mid, bird_down]
bird_index = 0
bird_flap = pygame.USEREVENT
pygame.time.set_timer(bird_flap, 200)
bird_img = birds[bird_index]
bird_rect = bird_img.get_rect(center=(56, 618 // 2))
bird_movement = 0
gravity = 0.16

# Memuat gambar pipa
pipe_img = pygame.image.load("C:\\Users\\Reaper\\Documents\\ASET GAME DEVPY\\Aset Objek\\Kayu.png")
pipe_height = [400, 350, 533, 490]

# Untuk memunculkan pipa
pipes = []
create_pipe = pygame.USEREVENT + 1
pygame.time.set_timer(create_pipe, 1100)

# Menampilkan gambar game over
game_over = False
over_img = pygame.image.load("C:\\Users\\Reaper\\Documents\\ASET GAME DEVPY\\Aset Objek\\front.png").convert_alpha ()
over_rect = over_img.get_rect(center=(width // 2, height // 2))

# Atur variabel dan font skor
score = 0
high_score = 0
score_time = True
score_font = pygame.font.Font("freesansbold.ttf", 27)

# Function untuk draw score
def draw_score(game_state):
    if game_state == "game_on":
        pygame.mixer.music.play(-1)
        score_text = score_font.render(str(score), True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(width // 2, 66))
        screen.blit(score_text, score_rect)

    elif game_state == "game_over":
        score_text = score_font.render(f" Score: {score}", True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(width // 2, 66))
        screen.blit(score_text, score_rect)

        high_score_text = score_font.render(f"High Score: {high_score}", True, (0, 0, 0))
        high_score_rect = high_score_text.get_rect(center=(width // 2, 506))
        screen.blit(high_score_text, high_score_rect)

# Function untuk mengupdate score
def score_update():
    global score, score_time, high_score
    if pipes:
        for pipe in pipes:
            if 65 < pipe.centerx < 69 and score_time:
                score += 1
                score_sound.play()
                score_time = False
            if pipe.left <= 0:
                score_time = True

    if score > high_score:
        high_score = score

# Game loop
running = True
while running:
    clock.tick(120)
    # untuk memeriksa tahapan program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # QUIT 
            running = False
            sys.exit()

        if event.type == pygame.KEYDOWN:  # Keyword 
            if event.key == pygame.K_SPACE and not game_over:  # If backspace adalah keyword
                lompat_sound.play()
                bird_movement = 0
                bird_movement = -7

            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                pipes = []
                bird_movement = 0
                bird_rect = bird_img.get_rect(center=(67, 600 // 2))
                score_time = True
                score = 0

        # Membuat tahapan yang berbeda
        if event.type == bird_flap:
            bird_index += 1
            if bird_index > 2:
                bird_index = 0

            bird_img = birds[bird_index]
            bird_rect = bird_up.get_rect(center=bird_rect.center)
        # Menambahkan pipa dalam daftar
        if event.type == create_pipe:
            pipes.extend(create_pipes())
    screen.blit(floor_img, (floor_x, 550))
    screen.blit(back_img, (0, 0))

    # Game over
    if not game_over:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = pygame.transform.rotozoom(bird_img, bird_movement * -6, 1)
        if bird_rect.top < 5 or bird_rect.bottom >= 550:
            game_over = True
        screen.blit(rotated_bird, bird_rect)
        pipe_animation()
        score_update()
        draw_score("game_on")
    elif game_over:
        screen.blit(over_img, over_rect)
        draw_score("game_over")

    # untuk memindahkan base
    floor_x -= 1
    if floor_x < -448:
        floor_x = 0

    draw_floor()

    # Update game window
    pygame.display.update()
# Menghentikan pygame dan sys
pygame.quit()
sys.exit()
