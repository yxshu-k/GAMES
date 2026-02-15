import pygame
import random
import sys

pygame.init()

# --------------------
# WINDOW SETUP
# --------------------
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Drift Runner")

clock = pygame.time.Clock()

# --------------------
# COLORS
# --------------------
BG_COLOR = (15, 15, 25)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 150)
WHITE = (240, 240, 240)

# --------------------
# PLAYER
# --------------------
player_width = 60
player_height = 100
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 150
player_speed = 6

# --------------------
# OBSTACLES
# --------------------
obstacles = []
obstacle_width = 60
obstacle_height = 100
obstacle_speed = 5

spawn_timer = 0

# --------------------
# SCORE
# --------------------
score = 0
font_big = pygame.font.SysFont("Arial", 40)
font_small = pygame.font.SysFont("Arial", 24)

# --------------------
# DRAW GLOW RECT
# --------------------
def draw_glow_rect(surface, color, rect):
    glow_surface = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
    pygame.draw.rect(glow_surface, (*color, 80), (10, 10, rect.width, rect.height), border_radius=15)
    surface.blit(glow_surface, (rect.x - 10, rect.y - 10))
    pygame.draw.rect(surface, color, rect, border_radius=15)

# --------------------
# GAME LOOP
# --------------------
running = True
game_over = False

while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                obstacles.clear()
                score = 0
                obstacle_speed = 5
                game_over = False

    keys = pygame.key.get_pressed()

    if not game_over:
        # Player movement
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Spawn obstacles
        spawn_timer += 1
        if spawn_timer > 40:
            lane_x = random.randint(0, WIDTH - obstacle_width)
            obstacles.append(pygame.Rect(lane_x, -100, obstacle_width, obstacle_height))
            spawn_timer = 0

        # Move obstacles
        for obstacle in obstacles:
            obstacle.y += obstacle_speed

        # Collision detection
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                game_over = True

        # Remove off-screen obstacles
        obstacles = [obs for obs in obstacles if obs.y < HEIGHT]

        # Increase difficulty
        score += 1
        if score % 500 == 0:
            obstacle_speed += 0.5

    # Draw player
    draw_glow_rect(screen, NEON_BLUE, pygame.Rect(player_x, player_y, player_width, player_height))

    # Draw obstacles
    for obstacle in obstacles:
        draw_glow_rect(screen, NEON_PINK, obstacle)

    # Score UI
    score_text = font_small.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))

    if game_over:
        over_text = font_big.render("GAME OVER", True, WHITE)
        restart_text = font_small.render("Press R to Restart", True, WHITE)
        screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
