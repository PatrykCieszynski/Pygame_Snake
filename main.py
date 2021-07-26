import pygame
from sys import exit
from random import randint
from pygame.math import Vector2


# Variables
DEFAULT_WIDTH = 935
DEFAULT_HEIGHT = 935
DEFAULT_FPS = 60
cellSize = 55
cellNumber = 17
clock = pygame.time.Clock()
pygame.font.init()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
pygame.display.set_caption('Snake')
screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT))


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load('Sprites/head_up.png').convert_alpha()
        self.head_up = pygame.transform.rotozoom(self.head_up, 0, 1.375)
        self.head_down = pygame.image.load('Sprites/head_down.png').convert_alpha()
        self.head_down = pygame.transform.rotozoom(self.head_down, 0, 1.375)
        self.head_right = pygame.image.load('Sprites/head_right.png').convert_alpha()
        self.head_right = pygame.transform.rotozoom(self.head_right, 0, 1.375)
        self.head_left = pygame.image.load('Sprites/head_left.png').convert_alpha()
        self.head_left = pygame.transform.rotozoom(self.head_left, 0, 1.375)

        self.tail_up = pygame.image.load('Sprites/tail_up.png').convert_alpha()
        self.tail_up = pygame.transform.rotozoom(self.tail_up, 0, 1.375)
        self.tail_down = pygame.image.load('Sprites/tail_down.png').convert_alpha()
        self.tail_down = pygame.transform.rotozoom(self.tail_down, 0, 1.375)
        self.tail_right = pygame.image.load('Sprites/tail_right.png').convert_alpha()
        self.tail_right = pygame.transform.rotozoom(self.tail_right, 0, 1.375)
        self.tail_left = pygame.image.load('Sprites/tail_left.png').convert_alpha()
        self.tail_left = pygame.transform.rotozoom(self.tail_left, 0, 1.375)

        self.body_vertical = pygame.image.load('Sprites/body_vertical.png').convert_alpha()
        self.body_vertical = pygame.transform.rotozoom(self.body_vertical, 0, 1.375)
        self.body_horizontal = pygame.image.load('Sprites/body_horizontal.png').convert_alpha()
        self.body_horizontal = pygame.transform.rotozoom(self.body_horizontal, 0, 1.375)

        self.body_tr = pygame.image.load('Sprites/body_tr.png').convert_alpha()
        self.body_tr = pygame.transform.rotozoom(self.body_tr, 0, 1.375)
        self.body_tl = pygame.image.load('Sprites/body_tl.png').convert_alpha()
        self.body_tl = pygame.transform.rotozoom(self.body_tl, 0, 1.375)
        self.body_br = pygame.image.load('Sprites/body_br.png').convert_alpha()
        self.body_br = pygame.transform.rotozoom(self.body_br, 0, 1.375)
        self.body_bl = pygame.image.load('Sprites/body_bl.png').convert_alpha()
        self.body_bl = pygame.transform.rotozoom(self.body_bl, 0, 1.375)
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            # 1. We need a rect for positioning
            block_rect = pygame.Rect(block.x * cellSize, block.y * cellSize, cellSize, cellSize)
            # 2. what direction is the face heading
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class APPLE:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cellSize, self.pos.y * cellSize, cellSize, cellSize)
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self):
        self.x = randint(0, cellNumber - 1)
        self.y = randint(0, cellNumber - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.apple = APPLE()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_element(self):
        self.apple.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.apple.pos == self.snake.body[0]:
            self.apple.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.apple.pos:
                self.apple.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cellNumber or not 0 <= self.snake.body[0].y < cellNumber:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surf = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cellSize * cellNumber - 70)
        score_y = int(cellSize * cellNumber - 70)
        score_rect = score_surf.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 10, apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surf, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

    def game_over(self):
        self.snake.reset()


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Graphics
apple = pygame.image.load('Sprites/apple.png').convert_alpha()
apple = pygame.transform.rotozoom(apple, 0, 1.325)

# Background
board = pygame.Surface((cellSize * cellNumber, cellSize * cellNumber))
board.fill('#aad751')
for x in range(0, cellNumber):
    for y in range(0, cellNumber, 2):
        if x % 2 == 0:
            pygame.draw.rect(board, '#a2d149', (x * cellSize, y * cellSize, cellSize, cellSize))
        else:
            pygame.draw.rect(board, '#a2d149', (x * cellSize, y * cellSize+cellSize, cellSize, cellSize))

# Timers
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

    screen.blit(board, board.get_rect())
    main_game.draw_element()
    pygame.display.update()
    clock.tick(DEFAULT_FPS)
