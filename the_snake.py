from random import choice

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
OPPOSITE_DIRECTIONS = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}
KEY_TO_DIRECTION = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
    pygame.K_w: UP,
    pygame.K_s: DOWN,
    pygame.K_a: LEFT,
    pygame.K_d: RIGHT
}

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 5
ALL_CELLS = {
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
}

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')


clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, color=None):
        self.position = CENTER_POSITION
        self.body_color = color

    def draw(self):
        """Метод для отрисовки объектов."""
        raise NotImplementedError(
            f'Метод draw не реализован в классе {type(self).__name__}'
        )

    def draw_cell(self, segment, color=None):
        """Отрисовка ячейки."""
        color = color or self.body_color
        rect = pygame.Rect(segment, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        if color not in (BORDER_COLOR, BOARD_BACKGROUND_COLOR):
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс для объекта яблока."""

    def __init__(
        self,
        occupied_positions=(),
        color=APPLE_COLOR
    ):
        super().__init__(color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Установка случайного положения яблока."""
        self.position = choice(tuple(ALL_CELLS - set(occupied_positions)))

    def draw(self):
        """Отрисовка яблока."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс для объекта змейки."""

    def __init__(self, color=SNAKE_COLOR):
        super().__init__(color)
        self.reset(direction=RIGHT)

    def get_head_position(self):
        """Метод возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Метод, который отвечает за движение змейки."""
        (head_x, head_y) = self.get_head_position()
        (direction_x, direction_y) = self.direction
        new_head = (
            (head_x + GRID_SIZE * direction_x) % SCREEN_WIDTH,
            (head_y + GRID_SIZE * direction_y) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self, next_direction):
        """Метод обновления направления после нажатия на кнопку."""
        if next_direction != OPPOSITE_DIRECTIONS[self.direction]:
            self.direction = next_direction

    def draw(self):
        """Метод отрисовки змейки."""
        self.draw_cell(self.get_head_position())
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def hits_self(self):
        """Проверяет на столкновение змейки с собой."""
        return self.get_head_position() in self.positions[2:]

    def reset(self, direction=None):
        """Возвращает змейку в начальное состояние."""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.last = None
        self.direction = direction or choice([UP, LEFT, DOWN, RIGHT])


def handle_keys(snake):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN and event.key in KEY_TO_DIRECTION:
            snake.update_direction(KEY_TO_DIRECTION[event.key])


def main():
    """Главный метод, точка входа."""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.hits_self():
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
