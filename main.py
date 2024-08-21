import pygame
import random


CELL_SIZE = 20
GRID_HSIZE = 20
GRID_VSIZE = 30

GAME_SPEED = 0.05
SNAKE_WIDTH = 0.9

SCREEN_WIDTH = CELL_SIZE * GRID_HSIZE
SCREEN_HEIGHT = CELL_SIZE * GRID_VSIZE

GAME_SPEED = 10 // GAME_SPEED

UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)

COLORS = [
    (240, 133, 133),
    (255, 173, 152),
    (65, 93, 133)
]

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
delta_time = 0
elapsed_time = 0


class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def xy(self):
        return (self._x, self._y) 

    @xy.setter
    def xy(self, value):
        self._x, self._y = value

    def __add__(self, point):
        return Point(
            self._x + point.x,
            self._y + point.y,
        )


class Snake:
    def __init__(self, head, size, direction):
        self._head = head
        self._size = size
        self._drtn = direction

    def up(self):
        self._drtn.xy = UP if self._drtn.xy != DOWN else DOWN

    def down(self):
        self._drtn.xy = DOWN if self._drtn.xy != UP else UP

    def right(self):
        self._drtn.xy = RIGHT if self._drtn.xy != LEFT else LEFT

    def left(self):
        self._drtn.xy = LEFT if self._drtn.xy != RIGHT else RIGHT

    def next(self):
        self._head += self._drtn
        return self._head


class Food:
    pass


class Cell:
    def __init__(self, x, y, color):
        pass


class Grid:
    def __init__(self, sc, width, height, cell_size):
        self._sc = sc
        self._width = width
        self._height = height
        self._cell_size = cell_size
        self._grid_matrix = list()

        for i in range(0, GRID_HSIZE):
            self._grid_matrix.append(list())
            for j in range(0, GRID_VSIZE):
                box = pygame.rect.Rect(
                    i * CELL_SIZE, 
                    j * CELL_SIZE, 
                    self._cell_size, 
                    self._cell_size
                )
                pygame.draw.rect(self._sc, COLORS[(i + j) % 2], box)
                self._grid_matrix[i].append(box)

    def draw_snake(self, x, y):
        pygame.draw.rect(
            self._sc, COLORS[2],
            self._grid_matrix[x][y].inflate(-2, -2),
        )


snake = Snake(Point(5, 5), 2, Point(0, 1))
grid = Grid(screen, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        snake.up()
    if keys[pygame.K_s]:
        snake.down()
    if keys[pygame.K_d]:
        snake.right()
    if keys[pygame.K_a]:
        snake.left()

    if elapsed_time > GAME_SPEED:
        grid.draw_snake(*snake.next().xy)
        elapsed_time = 0

    pygame.display.flip()

    delta_time = clock.tick(60)
    elapsed_time += delta_time

pygame.quit()
