import pygame
import sys
import heapq
from collections import deque
import random

# --------------------------
# CONFIG
# --------------------------
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
BLUE = (50, 150, 255)
RED = (255, 70, 70)
GREEN = (50, 255, 100)
YELLOW = (255, 255, 0)
PURPLE = (180, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Algorithm Arena - Escape the AI Grid")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# --------------------------
# GRID
# --------------------------
def create_grid():
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for i in range(ROWS):
        for j in range(COLS):
            if random.random() < 0.2:
                grid[i][j] = 1  # Wall
    return grid

def draw_grid(grid):
    for i in range(ROWS):
        for j in range(COLS):
            rect = pygame.Rect(j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[i][j] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, (200,200,200), rect, 1)

# --------------------------
# PATHFINDING
# --------------------------
def get_neighbors(node, grid):
    x, y = node
    neighbors = []
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = x+dx, y+dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and grid[nx][ny] == 0:
            neighbors.append((nx, ny))
    return neighbors

def bfs(grid, start, goal):
    queue = deque([start])
    came_from = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for neighbor in get_neighbors(current, grid):
            if neighbor not in came_from:
                queue.append(neighbor)
                came_from[neighbor] = current
    return reconstruct_path(came_from, start, goal)

def greedy(grid, start, goal):
    heap = []
    heapq.heappush(heap, (heuristic(start, goal), start))
    came_from = {start: None}
    while heap:
        _, current = heapq.heappop(heap)
        if current == goal:
            break
        for neighbor in get_neighbors(current, grid):
            if neighbor not in came_from:
                heapq.heappush(heap, (heuristic(neighbor, goal), neighbor))
                came_from[neighbor] = current
    return reconstruct_path(came_from, start, goal)

def astar(grid, start, goal):
    heap = []
    heapq.heappush(heap, (0, start))
    came_from = {start: None}
    cost = {start: 0}
    while heap:
        _, current = heapq.heappop(heap)
        if current == goal:
            break
        for neighbor in get_neighbors(current, grid):
            new_cost = cost[current] + 1
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(heap, (priority, neighbor))
                came_from[neighbor] = current
    return reconstruct_path(came_from, start, goal)

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def reconstruct_path(came_from, start, goal):
    if goal not in came_from:
        return []
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

# --------------------------
# GAME LOOP
# --------------------------
def main():
    level = 1
    grid = create_grid()
    player = (0, 0)
    enemy = (ROWS-1, COLS-1)
    portal = (ROWS-1, 0)

    grid[player[0]][player[1]] = 0
    grid[enemy[0]][enemy[1]] = 0
    grid[portal[0]][portal[1]] = 0

    running = True
    while running:
        screen.fill(WHITE)
        draw_grid(grid)

        # Draw Portal
        pygame.draw.rect(screen, PURPLE,
                         (portal[1]*CELL_SIZE, portal[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw Player
        pygame.draw.rect(screen, BLUE,
                         (player[1]*CELL_SIZE, player[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw Enemy
        pygame.draw.rect(screen, RED,
                         (enemy[1]*CELL_SIZE, enemy[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        text = font.render(f"Level: {level}", True, BLACK)
        screen.blit(text, (10, 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        x, y = player

        if keys[pygame.K_UP] and x > 0 and grid[x-1][y] == 0:
            player = (x-1, y)
        if keys[pygame.K_DOWN] and x < ROWS-1 and grid[x+1][y] == 0:
            player = (x+1, y)
        if keys[pygame.K_LEFT] and y > 0 and grid[x][y-1] == 0:
            player = (x, y-1)
        if keys[pygame.K_RIGHT] and y < COLS-1 and grid[x][y+1] == 0:
            player = (x, y+1)

        # Enemy Movement
        if level == 1:
            path = bfs(grid, enemy, player)
        elif level == 2:
            path = greedy(grid, enemy, player)
        else:
            path = astar(grid, enemy, player)

        if path:
            enemy = path[0]

        # Collision
        if enemy == player:
            print("Game Over!")
            pygame.quit()
            sys.exit()

        # Portal reached
        if player == portal:
            level += 1
            if level > 3:
                print("You defeated the AI!")
                pygame.quit()
                sys.exit()
            grid = create_grid()
            player = (0, 0)
            enemy = (ROWS-1, COLS-1)
            portal = (ROWS-1, 0)

        clock.tick(8)

if __name__ == "__main__":
    main()
