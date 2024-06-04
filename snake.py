import pygame
import sys
import random
pygame.font.init()
import time

class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.color = (17, 24, 47)
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x,y = self.direction
        new = (((cur[0]+(x*gridsize))%screen_width), (cur[1]+(y*gridsize))%screen_height)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0

    def draw(self,surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (gridsize,gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93,216, 228), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

class Food():
    def __init__(self):
        self.position = (0,0)
        self.color = (223, 163, 49)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, int(grid_width)-1)*gridsize, random.randint(0, int(grid_height)-1)*gridsize)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)


class SpecialFood():
    def __init__(self):
        self.position = (0, 0)
        self.color = (255, 0, 0)
        self.spawn_time = None

    def randomize_position(self):
        self.position = (random.randint(0, int(grid_width) - 1) * gridsize, random.randint(0, int(grid_height) - 1) * gridsize)
        self.spawn_time = time.time()

    def draw(self, surface):
        current_time = time.time()
        if int(current_time * 10) % 2 == 0:
            r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)

    def is_expired(self):
        return time.time() - self.spawn_time > 5

def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x + y)%2 == 0:
                r = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface,(93,216,228), r)
            else:
                rr = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, (84,194,205), rr)

screen_width = 720
screen_height = 720

gridsize = 30
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

STAT_FONT = pygame.font.SysFont("poppins", 50)

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
    pygame.display.set_caption('Snake')

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake()
    food = Food()
    special_food = SpecialFood()
    next_special_food_score = snake.score + random.randint(5, 10)
    special_food_active = False

    sound = pygame.mixer.Sound("bg-music-1.mp3")
    pygame.mixer.Sound.play(sound)
    myfont = pygame.font.SysFont("monospace",16)

    while (True):
        clock.tick(7)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()

        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()

            if snake.score >= next_special_food_score:
                special_food.randomize_position()
                special_food_active = True
        
        if special_food_active:
            if snake.get_head_position() == special_food.position:
                snake.score += 5
                special_food_active = False
                next_special_food_score = snake.score + random.randint(5, 10)
            elif special_food.is_expired():
                special_food_active = False
                next_special_food_score = snake.score + random.randint(5, 10)


        snake.draw(surface)
        food.draw(surface)

        if special_food_active:
            special_food.draw(surface)

        screen.blit(surface, (0,0))
        text = STAT_FONT.render("Score : {0}".format(snake.score), 5, (0,0,0))
        screen.blit(text, (5,10))
        pygame.display.update()

main()
