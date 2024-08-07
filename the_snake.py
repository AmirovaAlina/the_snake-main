from random import choice, randint

import pygame

# Константы для размеров поля и сетки:

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения:

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

random_directions = [UP, DOWN, LEFT, RIGHT]
starting_random_direction = choice(random_directions)



# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Snake by Alina')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    def __init__(self, position=SCREEN_CENTER, body_color=None):
        self.position = position
        self.body_color = body_color


    def draw(self):
        pass 


class Apple(GameObject):
    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (
            randint(0, GRID_WIDTH) * GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE
        )


    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    def __init__(self, next_direction=None, last=None):
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = starting_random_direction
        self.next_direction = next_direction
        self.last = last
        super().__init__(body_color=SNAKE_COLOR)

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        dx, dy = self.get_head_position()
        self.position = (
            (dx + (self.direction[0] * GRID_SIZE)) % SCREEN_WIDTH,
            (dy + (self.direction[1] * GRID_SIZE)) % SCREEN_HEIGHT)

        self.positions.insert(0, self.position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()


    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)


        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)   


    def get_head_position(self):
        return self.position
    

    def reset(self):
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.position = SCREEN_CENTER
        self.direction = starting_random_direction      


def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT

   
def main():
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    running = True

    while running:
        clock.tick(SPEED)  # Скорость игры
        snake.move()
        handle_keys(snake)
        snake.update_direction()
        apple.draw()
        snake.draw()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        # Проверка и сброс змеи если змея укусила себя.
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        # Проверка если змея съела яблоко.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()


if __name__ == '__main__':
    main()
