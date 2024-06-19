import pygame
from pygame.locals import *
from random import randint, choice

class Square(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Square, self).__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 200, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    def update(self):
        pass
    def move(self, x, y):
        self.rect.move_ip(x, y)

class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Food, self).__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.color = (255, 0, 0)
        self.position = (x, y)
    def randomise(self):
        # randomly to new location
        self.rect.center = (randint(10, 790)//20 * 20 + 10, randint(10, 590)//20 * 20 + 10)
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], 20, 20))

# snake is a collection of squares
class Snake(pygame.sprite.Group):
    def __init__(self, x, y):
        super(Snake, self).__init__()
        self.add(Square(x, y))
        self.direction = choice([(20, 0), (-20, 0), (0, 20), (0, -20)])
        self.positions = [(x, y)]
        self.length = 1
    def get_head_position(self):
        return self.positions[0]
    def turn(self, point): # cannot turn 180 degrees
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point
    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0]+x)%800), (cur[1]+y)%600)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
    def reset(self):
        self.empty()
        self.add(Square(400, 300))
        self.direction = choice([(20, 0), (-20, 0), (0, 20), (0, -20)])
    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, (randint(0,255), randint(0,255), randint(0,255)), (p[0], p[1], 20, 20))

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Snake')
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    snake = Snake(400, 300)
    food = Food(randint(10, 790)//20 * 20 + 10, randint(10, 590)//20 * 20 + 10)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    snake.turn((0, -20))
                if event.key == K_DOWN:
                    snake.turn((0, 20))
                if event.key == K_LEFT:
                    snake.turn((-20, 0))
                if event.key == K_RIGHT:
                    snake.turn((20, 0))
        snake.move()

        if -10 < snake.get_head_position()[0] - food.rect.center[0] < 10 and -10 < snake.get_head_position()[1] - food.rect.center[1] < 10:
            snake.length += 1
            food.randomise()
        
        surface.fill((0, 0, 0))
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(10)


if __name__ == '__main__':
    main()





