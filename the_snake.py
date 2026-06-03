from random import choice, randint

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
}

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 5

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
        if color is None:
            color = self.body_color
        rect = pygame.Rect(segment, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс для объекта яблока."""

    def __init__(
        self,
        occupied_positions=(CENTER_POSITION,),
        color=APPLE_COLOR
    ):
        super().__init__(color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Установка случайного положения яблока."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in occupied_positions:
                break

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
        dx, dy = (GRID_SIZE * direction_x, GRID_SIZE * direction_y)
        new_head = (
            (head_x + dx) % SCREEN_WIDTH,
            (head_y + dy) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = self.positions[-1]

    def update_direction(self, next_direction):
        """Метод обновления направления после нажатия на кнопку."""
        if (
            next_direction is not None
            and next_direction != OPPOSITE_DIRECTIONS[self.direction]
        ):
            self.direction = next_direction

    def draw(self):
        """Метод отрисовки змейки."""
        self.draw_cell(self.get_head_position())
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def hits_self(self):
        """Проверяет на столкновение змейки с собой."""
        head = self.get_head_position()
        return head in self.positions[1:]

    def reset(self, direction=None):
        """Возвращает змейку в начальное состояние."""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.last = None
        self.body_color = SNAKE_COLOR
        if direction is None:
            self.direction = choice([UP, LEFT, DOWN, RIGHT])
        else:
            self.direction = direction


def handle_keys(snake):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key in KEY_TO_DIRECTION:
                snake.update_direction(KEY_TO_DIRECTION[event.key])
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit


def handle_apple_collision(snake: Snake, apple: Apple):
    """Увеличивает размер змейки при поедании яблока."""
    if snake.get_head_position() == apple.position:
        snake.length += 1
        apple.randomize_position(snake.positions)


def main():
    """Главный метод, точка входа."""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        handle_apple_collision(snake, apple)
        if snake.hits_self():
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
