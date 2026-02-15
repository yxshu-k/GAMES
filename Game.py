import pygame
import random

# ----- YOUR GIVEN CLASS (OOP) -----
class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def attack(self, other):
        print(f"{self.name} attacks {other.name}!")
        other.health -= 10
        print(f"{other.name}'s health is now {other.health}")

# ----- PLAYER CLASS -----
class Player(Character):
    def __init__(self, name, health, x, y):
        super().__init__(name, health)
        self.x = x
        self.y = y
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

# ----- ENEMY CLASS -----
class Enemy(Character):
    def __init__(self, name, health, x, y):
        super().__init__(name, health)
        self.x = x
        self.y = y

# ----- GAME SETUP -----
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Mini Retro Attack Game")

font = pygame.font.SysFont(None, 28)

player = Player("Hero", 100, 50, 200)
enemy = Enemy("Monster", 100, random.randint(200,500), random.randint(50,350))

clock = pygame.time.Clock()

# ----- GAME LOOP -----
running = True
while running:
    screen.fill((20, 20, 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Attack when SPACE pressed near enemy
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if abs(player.x - enemy.x) < 40 and abs(player.y - enemy.y) < 40:
                    player.attack(enemy)

    keys = pygame.key.get_pressed()
    player.move(keys)

    # Draw Player & Enemy
    pygame.draw.rect(screen, (0, 255, 0), (player.x, player.y, 30, 30))
    pygame.draw.rect(screen, (255, 0, 0), (enemy.x, enemy.y, 30, 30))

    # Health Text
    p_text = font.render(f"Player HP: {player.health}", True, (255,255,255))
    e_text = font.render(f"Enemy HP: {enemy.health}", True, (255,255,255))
    screen.blit(p_text, (10,10))
    screen.blit(e_text, (450,10))

    # Win Condition
    if enemy.health <= 0:
        win = font.render("YOU WIN!", True, (255,255,0))
        screen.blit(win, (260,180))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
