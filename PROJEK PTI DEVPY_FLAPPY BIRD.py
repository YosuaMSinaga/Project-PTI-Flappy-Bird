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

        if burung1_rect.colliderect(pipe):
            game_over = True
# Game window
width, height = 350, 622
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

# Pengaturan background dan base image
back_img = pygame.image.load("C:\Flappy bird\\ASET GAME DEVPY\\Aset Objek\\background.png")
floor_img = pygame.image.load("C:\Flappy bird\\ASET GAME DEVPY\\Aset Objek\\Tanah.png")
floor_x = 0

# different stages of bird
burung1_up = pygame.image.load("C:\Flappy bird\\ASET GAME DEVPY\\Aset Objek\\B.png")
burung1_down = pygame.image.load("C:\Flappy bird\\ASET GAME DEVPY\\Aset Objek\\B1.png")
burung1_mid = pygame.image.load("C:\Flappy bird\\ASET GAME DEVPY\\Aset Objek\\B2.png")
burung = [burung1_up, burung1_mid, burung1_down]
burung1_index = 0
burung1_flap = pygame.USEREVENT
pygame.time.set_timer(burung1_flap, 200)
burung1_img = burung[burung1_index]
burung1_rect = burung1_img.get_rect(center=(56, 618 // 2))
burung1_movement = 0
gravity = 0.16

# Memuat gambar pipa
pipe_img = pygame.image.load("C:\Flappy bird\\ASET GAME DEVPY\\Aset Objek\\Kayu.png")
pipe_height = [400, 350, 533, 490]

# Untuk memunculkan pipa
pipes = []
create_pipe = pygame.USEREVENT + 1
pygame.time.set_timer(create_pipe, 1100)

# Menampilkan gambar game over
game_over = False
over_img = pygame.image.load("C:\Flappy bird\\ASET GAME DEVPY\\Aset Objek\\front.png").convert_alpha ()
over_rect = over_img.get_rect(center=(width // 2, height // 2))

# Atur variabel dan font skor
score = 0
high_score = 0
score_time = True
score_font = pygame.font.Font("freesansbold.ttf", 27)

# Fungsi untuk mencetak skor
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

# fungsi untuk mengupdate skor
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
                burung1_movement = 0
                burung1_movement = -7

            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                pipes = []
                burung1_movement = 0
                burung1_rect = burung1_img.get_rect(center=(67, 600 // 2))
                score_time = True
                score = 0

        # Membuat tahapan yang berbeda
        if event.type == burung1_flap:
            burung1_index += 1
            if burung1_index > 2:
                burung1_index = 0

            burung1_img = burung[burung1_index]
            burung1_rect = burung1_up.get_rect(center=burung1_rect.center)
        # Menambahkan pipa dalam daftar
        if event.type == create_pipe:
            pipes.extend(create_pipes())
    screen.blit(floor_img, (floor_x, 550))
    screen.blit(back_img, (0, 0))

    # Game over
    if not game_over:
        burung1_movement += gravity
        burung1_rect.centery += burung1_movement
        rotated_burung1 = pygame.transform.rotozoom(burung1_img, burung1_movement * -6, 1)
        if burung1_rect.top < 5 or burung1_rect.bottom >= 550:
            game_over = True
        screen.blit(rotated_burung1, burung1_rect)
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
