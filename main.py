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
    def __init__(self, x, y, color=None):
        self._x = x
        self._y = y
        self._color = color

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

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
            self.color)

    def __mod__(self, point):
        return Point(
            self._x % point.x,
            self._y % point.y,
            self.color)

    def __eq__(self, point):
        return (self.x, self.y) == (point.x, point.y)


class Snake:
    def __init__(self, head, size, direction, grid_corner):
        self._size = size
        self._drtn = direction
        self._grid_corner = grid_corner
        self._snake = [head]

        for i in range(size - 1):
            self._snake.append(self._snake[i] + self._drtn)

    @property
    def snake_points(self):
        return self._snake

    @property
    def head(self):
        return self._snake[0]

    def up(self):
        self._drtn.xy = UP if self._drtn.xy != DOWN else DOWN

    def down(self):
        self._drtn.xy = DOWN if self._drtn.xy != UP else UP

    def right(self):
        self._drtn.xy = RIGHT if self._drtn.xy != LEFT else LEFT

    def left(self):
        self._drtn.xy = LEFT if self._drtn.xy != RIGHT else RIGHT

    def grow(self, size):
        self._snake.extend((self._snake[-1],) * size)

    def next(self):
        self._snake.insert(0, (self.head + self._drtn) % self._grid_corner)
        return self.head, self._snake.pop()


class Feeder:
    def __init__(self, color, grid):
        self._color = color
        self._grid = grid
        self._food  = None

    def spawn_food(self, snake):
        filtered_grid = self._grid.copy()
        for point in snake:
                filtered_grid.remove(point)
        self._food = random.choice(filtered_grid)
        self._food.color = self._color
        return self._food

    def is_eaten(self, head):
        if self._food == head:
                return True
        return False


class Cell(pygame.rect.Rect):
    def __init__(self, x, y, side, color):
        self._color = color
        super().__init__(x, y, side, side)

    @property
    def color(self):
        return self._color


class Grid:
    def __init__(self, sc, rows, cols, cell_size, colors):
        self._sc = sc
        self._cell_matrix = [[Cell(
                x * cell_size, y * cell_size,
                    cell_size, colors[(x + y) % 2]) \
                        for y in range(cols)] for x in range(rows)]
        self._points = [Point(x, y) for x in range(rows) \
                                            for y in range(cols)]

        for point in self._points:
            cell = self._get_cell(point)
            pygame.draw.rect(self._sc, cell.color, cell)

    def _get_cell(self, point):
        return self._cell_matrix[point.x][point.y]

    @property
    def point_matrix(self):
        return self._points

    def draw_snake(self, head, tail):
        head_cell = self._get_cell(head)
        tail_cell = self._get_cell(tail)
        pygame.draw.rect(self._sc, head.color,
                                    head_cell.inflate(-2, -2))
        pygame.draw.rect(self._sc, tail_cell.color, tail_cell)

    def draw_food(self, point):
        food = self._get_cell(point)
        pygame.draw.rect(self._sc, point.color, food)


grid = Grid(screen, GRID_HSIZE, GRID_VSIZE, CELL_SIZE, COLORS)
snake = Snake(Point(5, 5, COLORS[2]), 2, Point(0, 1),
                                Point(GRID_HSIZE, GRID_VSIZE))
feeder = Feeder("red", grid.point_matrix)

grid.draw_food(feeder.spawn_food(snake.snake_points))

keys = pygame.key.get_pressed()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                pygame.time.wait(10000)

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
            grid.draw_food(feeder.spawn_food(snake.snake_points))
            snake.grow(1)
        elapsed_time = 0

    pygame.display.flip()

    delta_time = clock.tick(60)
    elapsed_time += delta_time

pygame.quit()
