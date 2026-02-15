import pygame
import sys
import time
import math
import random
import array

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1)

# ----------------------------
# WINDOW
# ----------------------------
WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TIME ECHO - Dynamic Music Edition")
clock = pygame.time.Clock()

# ----------------------------
# COLORS
# ----------------------------
BG = (12, 12, 25)
BLUE = (0, 255, 255)
PINK = (255, 0, 150)
GREEN = (0, 255, 120)
WHITE = (240, 240, 240)

# ----------------------------
# SOUND GENERATOR
# ----------------------------
def generate_wave(base_freq, wobble, speed, volume=0.2):
    sample_rate = 44100
    duration = 2
    n_samples = int(sample_rate * duration)
    buf = array.array("h")

    for s in range(n_samples):
        t = float(s) / sample_rate
        freq = base_freq + wobble * math.sin(2 * math.pi * speed * t)
        val = int(volume * 32767 * math.sin(2 * math.pi * freq * t))
        buf.append(val)

    return pygame.mixer.Sound(buffer=buf)

# Different BGMs
calm_bgm = generate_wave(180, 20, 1, 0.15)
medium_bgm = generate_wave(240, 40, 2, 0.2)
intense_bgm = generate_wave(320, 80, 4, 0.25)
danger_bgm = generate_wave(500, 120, 8, 0.3)

gameover_sound = generate_wave(120, 0, 1, 0.4)

current_music = None

def play_music(track):
    global current_music
    if current_music != track:
        pygame.mixer.stop()
        track.play(loops=-1)
        current_music = track

# ----------------------------
# PLAYER
# ----------------------------
size = 18
player_x = WIDTH // 2
player_y = HEIGHT // 2
speed = 5

movement_history = []
clones = []
particles = []

# ----------------------------
# LEVEL SYSTEM
# ----------------------------
level = 1
clone_delay = 5
clone_speed_multiplier = 1
last_clone_time = time.time()
start_time = 0

# ----------------------------
# FONTS
# ----------------------------
font_big = pygame.font.SysFont("Arial", 60, bold=True)
font_mid = pygame.font.SysFont("Arial", 28)
font_small = pygame.font.SysFont("Arial", 22)

# ----------------------------
# DRAW BACKGROUND GRID
# ----------------------------
def draw_grid():
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, (20, 20, 40), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, (20, 20, 40), (0, y), (WIDTH, y))

# ----------------------------
# DRAW PLAYER/CLONE
# ----------------------------
def draw_glow_rect(x, y, color):
    glow = pygame.Surface((size+16, size+16), pygame.SRCALPHA)
    pygame.draw.rect(glow, (*color, 80), (8,8,size,size), border_radius=6)
    screen.blit(glow, (x-8, y-8))
    pygame.draw.rect(screen, color, (x,y,size,size), border_radius=6)

def collision(x1,y1,x2,y2):
    return abs(x1-x2)<size and abs(y1-y2)<size

def is_danger():
    for clone in clones:
        if clone["index"] < len(clone["path"]):
            cx, cy = clone["path"][int(clone["index"])]
            if abs(cx-player_x)<40 and abs(cy-player_y)<40:
                return True
    return False

# ----------------------------
# GAME STATE
# ----------------------------
state = "menu"

# ----------------------------
# MAIN LOOP
# ----------------------------
running = True
while running:
    clock.tick(60)
    screen.fill(BG)
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            state = "game"
            movement_history.clear()
            clones.clear()
            particles.clear()
            start_time = time.time()

        if state == "gameover" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                state = "menu"

    if state == "menu":
        play_music(calm_bgm)
        title = font_big.render("TIME ECHO", True, BLUE)
        subtitle = font_mid.render("Click to Start", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//2))

    elif state == "game":
        survival_time = int(time.time() - start_time)

        # LEVEL CHANGE
        if survival_time > 20:
            level = 3
            clone_delay = 2
            clone_speed_multiplier = 2
            play_music(intense_bgm)
        elif survival_time > 10:
            level = 2
            clone_delay = 3
            clone_speed_multiplier = 1.5
            play_music(medium_bgm)
        else:
            level = 1
            clone_delay = 5
            clone_speed_multiplier = 1
            play_music(calm_bgm)

        if is_danger():
            play_music(danger_bgm)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: player_y -= speed
        if keys[pygame.K_DOWN]: player_y += speed
        if keys[pygame.K_LEFT]: player_x -= speed
        if keys[pygame.K_RIGHT]: player_x += speed

        player_x = max(0, min(WIDTH-size, player_x))
        player_y = max(0, min(HEIGHT-size, player_y))

        movement_history.append((player_x, player_y))

        if time.time() - last_clone_time > clone_delay:
            clones.append({"path": movement_history.copy(), "index": 0})
            last_clone_time = time.time()

        for clone in clones:
            if clone["index"] < len(clone["path"]):
                cx, cy = clone["path"][int(clone["index"])]
                draw_glow_rect(cx, cy, PINK)
                clone["index"] += clone_speed_multiplier

                if collision(player_x, player_y, cx, cy):
                    pygame.mixer.stop()
                    gameover_sound.play()
                    state = "gameover"

        draw_glow_rect(player_x, player_y, BLUE)

        level_text = font_small.render(f"Level: {level}", True, WHITE)
        time_text = font_small.render(f"Time: {survival_time}s", True, WHITE)
        screen.blit(level_text, (20, 20))
        screen.blit(time_text, (20, 50))

    elif state == "gameover":
        over = font_big.render("YOU MET YOUR PAST 😵", True, PINK)
        restart = font_mid.render("Press R to Return", True, WHITE)
        screen.blit(over, (WIDTH//2 - over.get_width()//2, HEIGHT//2 - 80))
        screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2))

    pygame.display.flip()

pygame.quit()
sys.exit()
