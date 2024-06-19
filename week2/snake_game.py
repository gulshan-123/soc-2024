import pygame
import sys
import random

# Game settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SQUARE_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WINDOW_WIDTH // 2), (WINDOW_HEIGHT // 2))]
        self.direction = random.choice([(-SQUARE_SIZE, 0), (SQUARE_SIZE, 0), (0, -SQUARE_SIZE), (0, SQUARE_SIZE)])
        self.color = GREEN

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0]+x)%WINDOW_WIDTH), (cur[1]+y)%WINDOW_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((WINDOW_WIDTH // 2), (WINDOW_HEIGHT // 2))]
        self.direction = random.choice([(-SQUARE_SIZE, 0), (SQUARE_SIZE, 0), (0, -SQUARE_SIZE), (0, SQUARE_SIZE)])

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], SQUARE_SIZE, SQUARE_SIZE))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, WINDOW_WIDTH//SQUARE_SIZE - 1)*SQUARE_SIZE, random.randint(0, WINDOW_HEIGHT//SQUARE_SIZE - 1)*SQUARE_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], SQUARE_SIZE, SQUARE_SIZE))

def play_game():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn((0, -SQUARE_SIZE))
                elif event.key == pygame.K_DOWN:
                    snake.turn((0, SQUARE_SIZE))
                elif event.key == pygame.K_LEFT:
                    snake.turn((-SQUARE_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.turn((SQUARE_SIZE, 0))

        snake.move()

        if snake.get_head_position() == food.position:
            snake.length += 1
            food.randomize_position()

        surface.fill((0,0,0))
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0,0))
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    play_game()