import pygame
import random

# Game configuration variables #

CELL_SIZE = 20
GRID_HSIZE = 20
GRID_VSIZE = 30

GAME_SPEED = 0.5
SNAKE_WIDTH = 0.9

# # # # # # # # # # # # # # # # 

SCREEN_WIDTH = CELL_SIZE * GRID_HSIZE
SCREEN_HEIGHT = CELL_SIZE * GRID_VSIZE

GAME_SPEED = 100 // GAME_SPEED

UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)

COLORS = [
    (240, 133, 133),
    (255, 173, 152),
    (65, 93, 133),
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
    def px(self):
        return self._x

    @property
    def py(self):
        return self._y

    @property
    def xy(self):
        return (self._x, self._y) 

    @xy.setter
    def xy(self, value):
        self._x, self._y = value

    def __add__(self, point):
        return Point(
            self._x + point.px,
            self._y + point.py)


class Snake:
    def __init__(self, head, size, direction, color, grid):
        self._size = size
        self._drtn = direction
        self._color = color
        self._grid = grid
        self._snake = [self._get_cell(head)]

        for i in range(0, size - 1):
            self._snake.insert(
                    0, self._get_cell(self._snake[i] + self._drtn))

    @property
    def snake_cells(self):
        return self._snake

    @property
    def head(self):
        return self._snake[-1]

    def _get_cell(self, point):
        return self._grid[point.px][point.py]

    def up(self):
        self._drtn.xy = UP if self._drtn.xy != DOWN else DOWN

    def down(self):
        self._drtn.xy = DOWN if self._drtn.xy != UP else UP

    def right(self):
        self._drtn.xy = RIGHT if self._drtn.xy != LEFT else LEFT

    def left(self):
        self._drtn.xy = LEFT if self._drtn.xy != RIGHT else RIGHT

    def grow(self, size):
        self._snake.extend((self.head,) * size)

    def next(self):
        self._snake.append(self._get_cell(self.head + self._drtn))
        return self.head, self._snake.pop(0)


class Feeder:
    def __init__(self, grid):
        self._flat_grid = grid
        self._food  = None

    def spawn_food(self, snake):
        filtered_grid = self._flat_grid.copy()
        for cell in snake:
            if cell not in filtered_grid:
                print(cell.px, cell.py)
            else:
                filtered_grid.remove(cell)
        self._food = random.choice(filtered_grid)
        return self._food

    def is_eaten(self, head):
        if self._food == head:
                return True
        return False


class Cell(pygame.rect.Rect, Point):
    def __init__(self, x, y, px, py, side, color):
        self._color = color
        super().__init__(x, y, side, side)
        Point.__init__(self, px, py)

    @property
    def color(self):
        return self._color
    ################ to be worked on #########
    def set_color(self, color):
        self._color = color
        return self


class Grid:
    def __init__(self, sc, rows, cols, cell_size):
        self._sc = sc
        self._cell_size = cell_size
        self._grid_matrix = [[Cell(
            x * self._cell_size, y * self._cell_size,
            x, y, self._cell_size, COLORS[(x + y) % 2]) \
            for y in range(cols)] for x in range(rows)]
        self._flat_grid = [i for j in self._grid_matrix for i in j]

        for cell in self._flat_grid:
            pygame.draw.rect(self._sc, cell.color, cell)

    @property
    def full_grid(self):
        return self._grid_matrix

    @property
    def flat_grid(self):
        return self._flat_grid

    def draw_snake(self, head, tail):
        pygame.draw.rect(self._sc, COLORS[2], head.inflate(-2, -2))
        pygame.draw.rect(self._sc, tail.color, tail)

    def draw_food(self, cell):
        pygame.draw.rect(self._sc, "red", cell)


grid = Grid(screen, GRID_HSIZE, GRID_VSIZE, CELL_SIZE)
snake = Snake(Point(5, 5), 2, Point(0, 1), COLORS[2], grid.full_grid)
feeder = Feeder(grid.flat_grid)

grid.draw_food(feeder.spawn_food(snake.snake_cells))

keys = pygame.key.get_pressed()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

    if elapsed_time > GAME_SPEED:
        if keys[pygame.K_w]:
            snake.up()
        if keys[pygame.K_s]:
            snake.down()
        if keys[pygame.K_d]:
            snake.right()
        if keys[pygame.K_a]:
            snake.left()

        head, tail = snake.next()
        grid.draw_snake(head, tail)
        if feeder.is_eaten(snake.head):
            grid.draw_food(feeder.spawn_food(snake.snake_cells))
            snake.grow(1)
        elapsed_time = 0

    pygame.display.flip()

    delta_time = clock.tick(60)
    elapsed_time += delta_time

pygame.quit()
