import pygame
from pygame.locals import *
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
myColor = (200, 190, 190)
dS = 20

class Square(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Square, self).__init__()
        self.surf = pygame.Surface((20,20))
        self.surf.fill(myColor)
        # self.rect = self.surf.get_rect()
        self.pos = [x, y]


pygame.init()
screen = pygame.display.set_mode((800, 600))
 
square = Square(20, 40)
x_food = random.randint(0,800)
y_food = random.randint(0,600)
food = Square(x_food, y_food)
screen.blit(food.surf, tuple(food.pos))
# Use blit to put something on the screen
screen.blit(square.surf, tuple(square.pos))

last_dir = (0, 0)

# Update the display using flip
pygame.display.flip()
gameOn = True
# Our game loop
while gameOn:
    squareRect = square.surf.get_rect(topleft=tuple(square.pos))
    foodRect = food.surf.get_rect(topleft=tuple(food.pos))
    # for loop through the event queue
    pygame.time.Clock().tick(10)
    for event in pygame.event.get():
        if event.type == QUIT:
            gameOn = False
    keys = pygame.key.get_pressed()
    square.surf.fill(BLACK)
    screen.blit(square.surf, tuple(square.pos)) # Remove old square
    square.surf.fill(myColor)
    if keys[K_w] or keys[K_UP]:
        # square.pos[1] -= dS
        last_dir = (0, -1)
        # keys[K_w] = False
        # keys[K_UP] = False
    if keys[K_a] or keys[K_LEFT]:
        # square.pos[0] -= dS
        last_dir = (-1, 0)
        # keys[K_a] = False
        # keys[K_LEFT] = False
    if keys[K_s] or keys[K_DOWN]:
        # square.pos[1] += dS
        last_dir = (0, 1)
        # keys[K_s] = False
        # keys[K_DOWN] = False
    if keys[K_d] or keys[K_RIGHT]:
        # square.pos[0] += dS
        last_dir = (1,0)
        # keys[K_d] = False
        # keys[K_RIGHT] = False
    square.pos[0] += dS*last_dir[0]
    square.pos[1] += dS*last_dir[1]
# Right edge collision
    if squareRect.right > 800:
        square.pos[0] = 800 - squareRect.width  # Move the square back within the right edge

    # Top edge collision
    if squareRect.top < 0:
        square.pos[1] = 0  # Move the square down to be within the top edge

    # Update square position
    squareRect.topleft = square.pos
    if ((squareRect.collidepoint(foodRect.centerx, foodRect.centery))):
        food.kill()
        x_food = random.randint(0,800)
        y_food = random.randint(0,600)
        food = Square(x_food, y_food)
    screen.fill((0,0,0))
    screen.blit(food.surf, tuple(food.pos))
    screen.blit(square.surf, tuple(square.pos)) # Put new square
    # Update the display using flip
    pygame.display.flip()

pygame.quit()