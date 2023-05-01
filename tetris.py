import pygame
import sys
import random

# Constants
BLOCK_SIZE = 40
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = GRID_WIDTH * BLOCK_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE
FPS = 4
MOVE_DOWN_EVENT = pygame.USEREVENT + 1
MOVE_DOWN_INTERVAL = 500  # Move the shape down every 500 milliseconds

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
COLORS = [RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1], [1, 1], [1, 1]],  # 3x2
[[1, 1, 1], [1, 1, 1], [1, 1, 1]],  # 3x3
[[1, 1, 1, 1 , 1, 1]], #MONSTER 6x1
[[1, 0, 1 ], [0, 1, 0], [ 1, 0, 1], [0, 1, 0], [1, 0, 1]], #MONSTER
    [[1, 1, 1], [0, 1, 0]],  # T
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]]  # L
]
class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)

    def draw(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color, (
                        self.x * BLOCK_SIZE + x * BLOCK_SIZE, self.y * BLOCK_SIZE + y * BLOCK_SIZE, BLOCK_SIZE,
                        BLOCK_SIZE), 0)

    def rotate(self):
        # Transpose the shape matrix
        self.shape = list(map(list, zip(*self.shape)))
        # Reverse each row to rotate clockwise
        self.shape = [row[::-1] for row in self.shape]


def create_tetromino():
    shape = random.choice(SHAPES)
    x = GRID_WIDTH // 2 - len(shape[0]) // 2
    y = 0
    return Tetromino(x, y, shape)

def remove_full_lines(grid):
    lines_removed = 0
    for y in range(GRID_HEIGHT - 1, -1, -1):
        if all(cell for cell in grid[y]):
            grid.pop(y)
            grid.insert(0, [None] * GRID_WIDTH)
            lines_removed += 1
    return lines_removed

def game_over(grid):
    return any(cell for cell in grid[0])
def draw_grid():
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))

def draw_score(score=0):
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))
def valid_move(tetromino, grid):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                if tetromino.y + y >= GRID_HEIGHT or tetromino.x + x < 0 or tetromino.x + x >= GRID_WIDTH or \
                        grid[tetromino.y + y][tetromino.x + x]:
                    return False
    return True

def merge_tetromino(tetromino, grid):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[tetromino.y + y][tetromino.x + x] = tetromino.color

def update_score(lines_removed):
    global score
    score += lines_removed * 100

def handle_input(event, current_tetromino, grid):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            current_tetromino.x -= 1
            if not valid_move(current_tetromino, grid):
                current_tetromino.x += 1
        elif event.key == pygame.K_RIGHT:
            current_tetromino.x += 1
            if not valid_move(current_tetromino, grid):
                current_tetromino.x -= 1
        elif event.key == pygame.K_DOWN:
            while valid_move(current_tetromino, grid):
                current_tetromino.y += 1
            current_tetromino.y -= 1
            merge_tetromino(current_tetromino, grid)
            lines_removed = remove_full_lines(grid)
            update_score(lines_removed)
            current_tetromino = create_tetromino()
        elif event.key == pygame.K_UP:  # Rotate the tetromino clockwise
            current_tetromino.rotate()
            if not valid_move(current_tetromino, grid):
                # Try moving the tetromino to the left
                current_tetromino.x -= 1
                if not valid_move(current_tetromino, grid):
                    # Try moving the tetromino to the right
                    current_tetromino.x += 2
                    if not valid_move(current_tetromino, grid):
                        # Rotate the tetromino back to its original position
                        current_tetromino.rotate()
                        current_tetromino.rotate()
                        current_tetromino.rotate()

    return current_tetromino, grid

def update_game_state(current_tetromino, grid):
    current_tetromino.y += 1
    if not valid_move(current_tetromino, grid):
        current_tetromino.y -= 1
        merge_tetromino(current_tetromino, grid)
        lines_removed = remove_full_lines(grid)
        update_score(lines_removed)
        current_tetromino = create_tetromino()

    return current_tetromino, grid
def game_loop():
    global score
    score = 0

    grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    current_tetromino = create_tetromino()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            current_tetromino, grid = handle_input(event, current_tetromino, grid)

        current_tetromino, grid = update_game_state(current_tetromino, grid)

        if game_over(grid):
            break

        screen.fill(BLACK)
        draw_grid()
        current_tetromino.draw()

        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        draw_score(score)
        pygame.display.update()
        clock.tick(FPS)
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    pygame.time.set_timer(MOVE_DOWN_EVENT, MOVE_DOWN_INTERVAL)
    game_loop()
