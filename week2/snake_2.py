import pygame
from pygame.locals import *
import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SNAKE_COLOR = (200, 190, 190)
FOOD_COLOR = (255, 0, 0)
SQUARE_SIZE = 20

class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, color=SNAKE_COLOR):
        super(Square, self).__init__()
        self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))  # Renamed 'surf' to 'image'
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))  # Use 'self.image' instead of 'self.surf'
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Create the snake
snake = pygame.sprite.Group()
head = Square(400, 300)
snake.add(head)

# Create the food
x_food = random.randint(0, 800 - SQUARE_SIZE)//SQUARE_SIZE * SQUARE_SIZE
y_food = random.randint(0, 600 - SQUARE_SIZE)//SQUARE_SIZE * SQUARE_SIZE
food = Square(x_food, y_food, FOOD_COLOR)

direction = (0, 0)
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            # Up or w
            if event.key in (K_UP, K_w) and direction != (0, SQUARE_SIZE):
                direction = (0, -SQUARE_SIZE)
            # Down or s
            if event.key in (K_DOWN, K_s) and direction != (0, -SQUARE_SIZE):
                direction = (0, SQUARE_SIZE)
            # Left or a
            if event.key in (K_LEFT, K_a) and direction != (SQUARE_SIZE, 0):
                direction = (-SQUARE_SIZE, 0)
            # Right or d
            if event.key in (K_RIGHT, K_d) and direction != (-SQUARE_SIZE, 0):
                direction = (SQUARE_SIZE, 0)
    # Move the snake
    for square in snake:
        if (snake.sprites().index(square) == 0):
            square.rect.move_ip(direction)
        else: 


    # Check if the snake is along the screen boundaries
    if not screen.get_rect().contains(snake.sprites()[0].rect):
        running = False
    # Check if the snake has collided with the food
    if pygame.sprite.spritecollideany(snake.sprites()[0], [food]):
        x_food = random.randint(0, 800 - SQUARE_SIZE)//SQUARE_SIZE * SQUARE_SIZE
        y_food = random.randint(0, 600 - SQUARE_SIZE)//SQUARE_SIZE * SQUARE_SIZE
        food.rect.topleft = (x_food, y_food)
        # Add a new square to the snake back at the previous position of the tail
        tail = snake.sprites()[-1]
        new_tail = Square(tail.rect.x-direction[0], tail.rect.y-direction[1])
        snake.add(new_tail)


    # Check if the snake has collided with itself
    pygame.time.Clock().tick(10)

    # Draw everything
    screen.fill(BLACK)
    snake.draw(screen)
    screen.blit(food.image, food.rect)
    pygame.display.flip()

pygame.quit()