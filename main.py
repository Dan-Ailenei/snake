import random
from collections import deque

import enum

DELTA_USER_INPUT = 1
INITIAL_SNAKE_SPEED = 2
INITIAL_SNAKE_LENGTH = 3

WINDOW_WIDTH, WINDOW_HEIGHT = 5, 5


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        return type(self)(other.x + self.x, other.y + self.y)

    def __repr__(self):
        return f'({self.x} {self.y})'


class Direction(enum.Enum):

    LEFT = Coordinate(-1, 0)
    RIGHT = Coordinate(1, 0)
    TOP = Coordinate(0, -1)
    DOWN = Coordinate(0, 1)

    @classmethod
    def get_random_direction(cls):
        directions = list(cls)
        return directions[random.randint(0, len(directions) - 1)]


class State:
    def __init__(self, snakes):
        self.snakes = snakes
        self.obstacles = set()
        self.bonuses = set()


def get_neighbours_for_coordonate(body, coord):
    neighbours = [coord + direction.value for direction in Direction]
    return {
        neighbour
        for neighbour in neighbours
        if (0 <= neighbour.x <= WINDOW_WIDTH)
           and (0 <= neighbour.y <= WINDOW_HEIGHT)
           and neighbour not in body
    }


class Snake:
    def __init__(self, body, direction, speed):
        self.body = body
        self.direction = direction
        self.speed = speed

    @classmethod
    def get_initial_snake(cls, length):
        body = deque()
        current_coordinate = Coordinate(
            random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)
        )
        body.append(current_coordinate)
        length -= 1
        while length:
            neighbours = get_neighbours_for_coordonate(body, current_coordinate)
            body.append(random.sample(neighbours, 1)[0])
            length -= 1
        return cls(body, Direction.get_random_direction(), INITIAL_SNAKE_SPEED)


def main():
    snake = Snake.get_initial_snake(INITIAL_SNAKE_LENGTH)
    state = State([snake])
    print(snake.body)
    draw_state(state)


def draw_state(state):
    for y in range(WINDOW_HEIGHT + 1):
        for x in range(WINDOW_HEIGHT + 1):
            for snake in state.snakes:
                if Coordinate(x=x, y=y) not in snake.body:
                    print(' ', end='')
                else:
                    print('*', end='')
        print()


main()
