import pygame
import sys
import random
import pygame_menu

# Ініціалізація pygame
pygame.init()

# Визначення кольорів та інших констант
SIZE_BLOCK = 20
FRAME_COLOR = (0, 255, 204)
WHITE = (255, 255, 255)
BLUE = (204, 255, 255)
RED = (224, 0, 0)
HEADER_COLOR = (0, 204, 153)
SNAKE_COLOR = (0, 102, 0)
COUNT_BLOCKS = 20
HEADER_MARGIN = 70
MARGIN = 1

# Завантаження фону
bg_image = pygame.image.load("snake.png")

# Визначення розмірів екрану
size = (SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS + HEADER_MARGIN)
print(size)

# Функція для малювання блоку на екрані
def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                                     HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1),
                                     SIZE_BLOCK,
                                     SIZE_BLOCK])

# Налаштування екрану та заголовка
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Змейка")

# Налаштування годинника для контролю частоти кадрів
timer = pygame.time.Clock()

# Визначення шрифту для тексту
courier = pygame.font.SysFont('courier', 36)


# Клас для блоку змії
class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        # Перевірка, чи знаходиться блок всередині ігрового поля
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other):
        # Перевірка на рівність з іншим блоком змії
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y

# Функція для запуску гри
def start_the_game():
    def get_random_empty_block():
        # Генерація випадкового блоку, що не перетинається зі змією
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
            empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return empty_block

    # Ініціалізація змії та яблука
    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
    apple = get_random_empty_block()
    d_row = buf_row = 0
    d_col = buf_col = 1
    total = 0
    speed = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("exit")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Обробка подій клавіатури для зміни напрямку руху змії
                if event.key == pygame.K_UP and d_col != 0:
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    buf_row = 1
                    buf_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_col = 1

        # Заповнення екрану фоновим кольором
        screen.fill(FRAME_COLOR)
        # Малювання заголовка
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

        # Відображення поточного рахунку та швидкості
        text_total = courier.render(f"Total: {total}", 0, WHITE)
        text_speed = courier.render(f"Speed: {speed}", 0, WHITE)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK + 250, SIZE_BLOCK))

        # Малювання ігрового поля
        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (row + column) % 2 == 0:
                    color = BLUE
                else:
                    color = WHITE
                draw_block(color, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            print("crash")
            return

        # Малювання яблука та змії
        draw_block(RED, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        # Перевірка на зіткнення з яблуком
        if apple == head:
            total += 1
            speed = total // 5 + 1
            snake_blocks.append(apple)
            apple = get_random_empty_block()
        else:
            snake_blocks.pop(0)

        # Оновлення напрямку руху змії
        d_row = buf_row
        d_col = buf_col
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        # Перевірка на зіткнення з самою собою
        if new_head in snake_blocks:
            print("crash yourself")
            return

        snake_blocks.append(new_head)

        pygame.display.flip()  # Оновлення екрану
        timer.tick(3 + speed)  # Контроль частоти кадрів


# Створення меню
menu = pygame_menu.Menu('Welcome', 400, 300, theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input("Name :", default='Player 1')  # Поле вводу імені
menu.add.button('Play', start_the_game)  # Кнопка для початку гри
menu.add.button('Exit', pygame_menu.events.EXIT)  # Кнопка для виходу

# Головний цикл
while True:
    screen.blit(bg_image, (0, 0))  # Відображення фону

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if menu.is_enabled():
        menu.update(events)  # Оновлення меню
        menu.draw(screen)  # Малювання меню

    pygame.display.update()  # Оновлення екрану