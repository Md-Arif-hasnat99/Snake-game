import pygame
import sys
import random

# Initialize
pygame.init()
clock = pygame.time.Clock()

# Game settings
CELL_SIZE = 25
GRID_WIDTH = 24
GRID_HEIGHT = 20
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT

# Colors
BG_COLOR = (30, 30, 30)
SNAKE_COLOR = (0, 200, 0)
FOOD_COLOR = (220, 30, 30)
GRID_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)

# Fonts
font = pygame.font.SysFont("comicsansms", 30)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game - Graphics Edition")

# Snake class
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
        self.direction = (1, 0)
        self.grow = False

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        if self.grow:
            self.body = [new_head] + self.body
            self.grow = False
        else:
            self.body = [new_head] + self.body[:-1]

    def change_direction(self, new_dir):
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def draw(self):
        for segment in self.body:
            x, y = segment
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, SNAKE_COLOR, rect, border_radius=8)

    def check_collision(self):
        head = self.body[0]
        return (
            head in self.body[1:] or
            head[0] < 0 or head[0] >= GRID_WIDTH or
            head[1] < 0 or head[1] >= GRID_HEIGHT
        )

# Food class
class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self):
        x, y = self.position
        rect = pygame.Rect(x * CELL_SIZE + 5, y * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10)
        pygame.draw.ellipse(screen, FOOD_COLOR, rect)

    def relocate(self, snake_body):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_body:
                self.position = pos
                break

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def show_text(text, size=40, y_offset=0, color=TEXT_COLOR):
    font_big = pygame.font.SysFont("comicsansms", size)
    label = font_big.render(text, True, color)
    rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(label, rect)

def game_over_screen(score):
    screen.fill(BG_COLOR)
    show_text("GAME OVER", 50, -40, (255, 80, 80))
    show_text(f"Score: {score}", 35, 20)
    show_text("Press R to Restart or Q to Quit", 25, 80, (200, 200, 200))
    pygame.display.update()

def game_loop():
    snake = Snake()
    food = Food()
    score = 0
    running = True

    while running:
        clock.tick(12)
        screen.fill(BG_COLOR)
        draw_grid()

        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_UP]:
                    snake.change_direction((0, -1))
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    snake.change_direction((0, 1))
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    snake.change_direction((-1, 0))
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    snake.change_direction((1, 0))

        # Move snake
        snake.move()

        # Eat food
        if snake.body[0] == food.position:
            score += 1
            snake.grow = True
            food.relocate(snake.body)

        # Check collision
        if snake.check_collision():
            break

        # Draw everything
        food.draw()
        snake.draw()

        score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))

        pygame.display.update()

    # Game over loop
    while True:
        game_over_screen(score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Start
game_loop()
