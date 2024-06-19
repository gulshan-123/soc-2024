import pygame
import sys
import random
from pygame.sprite import Sprite

# Game settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SQUARE_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

class ScoreBar:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        surface.blit(score_text, (10, 10))

    def update_score(self, points):
        self.score += points
class Snake(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2 + 10, WINDOW_HEIGHT // 2 + 10)
        self.direction = random.choice([(-SQUARE_SIZE, 0), (SQUARE_SIZE, 0), (0, -SQUARE_SIZE), (0, SQUARE_SIZE)])
        self.body = []
        self.length = 1
        self.last_direction = self.direction
        self.current_key = None

    def update(self):
        # Convert body positions to Rect objects
        next_position = self.rect.move(self.direction)
        if not pygame.display.get_surface().get_rect().contains(next_position):
            return False
        self.rect = next_position
        self.body.insert(0, self.rect.topleft)
        if len(self.body) > self.length:
            self.body.pop()
        return True

    def draw(self, surface):
            for part in self.body:
                r,g,b = (255,255,255) if part == self.body[0] else (0,255,0)
                pygame.draw.rect(surface, (r,g,b), (part[0], part[1], SQUARE_SIZE, SQUARE_SIZE))

class Food(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self):
        x = random.choice(range(0, WINDOW_WIDTH, SQUARE_SIZE))
        y = random.choice(range(0, WINDOW_HEIGHT, SQUARE_SIZE))
        self.rect.topleft = (x, y)
    def draw(self, surface):
        surface.blit(self.image, self.rect)

def play_game():
    foodEaten = 0
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)

    snake = Snake()

    food = Food()

    score_bar = ScoreBar()

    danger_food_group = pygame.sprite.Group()


    for _ in range(100):
        dangerFood = Food()
        dangerFood.image.fill(RED)
        dangerFood.randomize_position()
        danger_food_group.add(dangerFood)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                last_direction = snake.direction
                if event.key == pygame.K_UP and last_direction != (0, SQUARE_SIZE):
                    snake.direction = (0, -SQUARE_SIZE)
                    last_direction = (0, -SQUARE_SIZE)
                elif event.key == pygame.K_DOWN and last_direction != (0, -SQUARE_SIZE):
                    snake.direction = (0, SQUARE_SIZE)
                    last_direction = (0, SQUARE_SIZE)
                elif event.key == pygame.K_LEFT and last_direction != (SQUARE_SIZE, 0):
                    snake.direction = (-SQUARE_SIZE, 0)
                    last_direction = (-SQUARE_SIZE, 0)
                elif event.key == pygame.K_RIGHT and last_direction != (-SQUARE_SIZE, 0):
                    snake.direction = (SQUARE_SIZE, 0)
                    last_direction = (SQUARE_SIZE, 0)
        running = snake.update()
        if not running:
            print("Game Over!")
            print(f"Your score: {score_bar.score}")
            break

        body_rects = [pygame.Rect(pos[0], pos[1], snake.rect.width, snake.rect.height) for pos in snake.body[1:]]
        if snake.rect.colliderect(food.rect):
            foodEaten += 1
            snake.length += 1
            food.randomize_position()
            if (pygame.time.get_ticks()//1000) % 10 in [5,6,7]:
                score_bar.update_score((20 * (8 - ((pygame.time.get_ticks()//1000) % 10))))
            else:
                score_bar.update_score(10)

            while(food.rect in body_rects):
                # print("Error in food placement")
                # sys.exit()
                food.randomize_position()
        if snake.rect.collidelist(body_rects) != -1:
            # Find the index of the collision
            collision_index = snake.rect.collidelist(body_rects)
            old_length = snake.length
            # Remove the tail up to the point of collision
            snake.body = snake.body[:collision_index+2]
            snake.length = len(snake.body)
            new_length = snake.length
            # number of parts reduced
            score_bar.update_score((new_length-old_length)*15)
        
        

        screen.fill((0,0,0))
        snake.draw(screen)
        food.draw(screen)

        if ((pygame.time.get_ticks()//1000) % 10) in [5,6,7]:
            food.image.fill('yellow')
        else:
            food.image.fill(BLUE)

        numOfRedFood = foodEaten//5 % 12
        for danger_food in list(danger_food_group)[:numOfRedFood]:
            danger_food.draw(screen)
            while (danger_food.rect in body_rects) or (danger_food.rect == food.rect):
                danger_food.randomize_position()
                # print("Danger food placed on snake or food! but it's okay, I fixed it.")

            if snake.rect.colliderect(danger_food.rect):
                print("Game Over!")
                print(f"Your score: {score_bar.score}")
                running = False
                break
        score_bar.draw(screen)
        # print(len(snake.body))
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    play_game()