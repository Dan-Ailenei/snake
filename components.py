import random
from collections import deque

import enum
import settings


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
    def __init__(self, snakes, obstacles):
        self.snakes = snakes
        self.obstacles = obstacles
        self.bonuses = set()

    @classmethod
    def get_initial_state(cls):
        obstacles = cls.get_inital_obstacles()
        snake = cls.get_initial_snake(settings.INITIAL_SNAKE_LENGTH, obstacles)
        state = cls([snake], obstacles)

        return state

    @classmethod
    def get_inital_obstacles(cls):
        window_with = settings.WINDOW_WIDTH
        window_height = settings.WINDOW_HEIGHT

        obstacles = set()
        for i in range(window_height):
            obstacles.add(Coordinate(i, 0))
            obstacles.add(Coordinate(i, window_with - 1))

        for i in range(window_with):
            obstacles.add(Coordinate(0, i))
            obstacles.add(Coordinate(window_height - 1, i))

        return obstacles

    @classmethod
    def get_initial_snake(cls, length, obstacles):
        body = deque()

        # TODO : verify that it isn't in obstacles
        current_coordinate = Coordinate(
            random.randint(0, settings.WINDOW_WIDTH - 1), random.randint(0, settings.WINDOW_HEIGHT - 1)
        )
        body.append(current_coordinate)
        length -= 1
        while length:
            neighbours = get_neighbours_for_coordinate(
                set(body) | obstacles, current_coordinate
            )
            current_coordinate = neighbours[random.randint(0, len(neighbours) - 1)]
            body.append(current_coordinate)
            length -= 1
        return Snake(body, Direction.get_random_direction(), settings.INITIAL_SNAKE_SPEED)


def get_neighbours_for_coordinate(body, coord):
    neighbours = [coord + direction.value for direction in Direction]
    return [
        neighbour
        for neighbour in neighbours
        if (0 <= neighbour.x < settings.WINDOW_WIDTH)
           and (0 <= neighbour.y < settings.WINDOW_HEIGHT)
           and neighbour not in body
    ]


class Snake:
    def __init__(self, body, direction, speed):
        self.body = body
        self.direction = direction
        self.speed = speed


def draw_state(state):
    for y in range(settings.WINDOW_HEIGHT + 1):
        for x in range(settings.WINDOW_HEIGHT + 1):
            current_coordinate = Coordinate(x=x, y=y)
            if current_coordinate in state.obstacles:
                print('$', end='')
                continue

            for snake in state.snakes:
                if current_coordinate not in snake.body:
                    print(' ', end='')
                else:
                    print('*', end='')
        print()
