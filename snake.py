# File: snake.py
# Author: glatavento
# Date: 2021/1/5 下午8:01

import sys
from collections import deque, namedtuple
from random import randint
from typing import Literal, Deque

import pygame
from pampy import match

Point = namedtuple('Point', 'x y')


class SnakeGame:
    def __init__(self, x_len: int = 32, y_len: int = 24, speed: int = 5, no_wall: bool = False):
        self.x_len, self.y_len, self.speed, self.no_wall = x_len, y_len, speed, no_wall
        self.snake_body: Deque[Point] = deque([Point(2, 2), Point(2, 3), Point(2, 4)])
        self.snake_direct: Literal['U', 'D', 'L', 'R'] = 'R'
        self.food = self.gen_food()

    def gen_food(self) -> Point:
        while True:
            food = Point(randint(0, self.x_len - 1), randint(0, self.y_len - 1))
            if food not in self.snake_body:
                return food

    def next_turn(self) -> Literal['Stuck', 'Win', 'Next']:
        x, y = self.snake_body[-1]
        x = match(self.snake_direct, 'U', x, 'D', x, 'L', x - 1, 'R', x + 1)
        y = match(self.snake_direct, 'L', y, 'R', y, 'U', y - 1, 'D', y + 1)
        next_place = Point(x, y)
        if not 0 <= x < self.x_len or not 0 <= y < self.y_len:
            if self.no_wall:
                x = 0 if x >= self.x_len else self.x_len if x < 0 else x  # 处理穿墙部分
                y = 0 if y >= self.y_len else self.y_len if y < 0 else y  #
                next_place = Point(x, y)
            else:
                return 'Stuck'
        if next_place in self.snake_body:
            return 'Stuck'
        elif next_place == self.food:
            self.snake_body.append(next_place)
            if len(self.snake_body) == self.x_len * self.y_len:
                return 'Win'
            self.food = self.gen_food()
            return 'Next'
        else:
            self.snake_body.append(next_place)
            self.snake_body.popleft()
            return 'Next'

    def new_game(self) -> 'SnakeGame':
        return SnakeGame(self.x_len, self.y_len, self.speed, self.no_wall)


def main():
    def draw_rect(surface, color, point: Point):
        pygame.draw.rect(surface, color, (point.x * 20, point.y * 20, 20, 20), 0)

    game = SnakeGame(10, 10, 5, True)
    pygame.init()
    display = pygame.display.set_mode((game.x_len * 20, game.y_len * 20))
    pygame.display.set_caption('Snake')
    fps_clock = pygame.time.Clock()
    next_direct = game.snake_direct

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                next_direct = match(e.key,
                                    pygame.K_UP, 'U', pygame.K_w, 'U',
                                    pygame.K_DOWN, 'D', pygame.K_s, 'D',
                                    pygame.K_LEFT, 'L', pygame.K_a, 'L',
                                    pygame.K_RIGHT, 'R', pygame.K_d, 'R')
        if game.snake_direct + next_direct not in ('UD', 'DU', 'LR', 'RL'):
            game.snake_direct = next_direct  # 更新方向
        status = game.next_turn()
        if status != 'Next':
            game = game.new_game()
        display.fill('#FFFFFF')  # 白色背景
        for p in game.snake_body:
            draw_rect(display, '#000000', p)  # 黑色
        draw_rect(display, '#FF0000', game.food)  # 红色
        pygame.display.update()
        fps_clock.tick(game.speed)


if __name__ == '__main__':
    main()
