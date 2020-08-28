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

    @classmethod
    def get_random_coordinate(cls):
        return cls(
            random.randint(0, settings.WINDOW_HEIGHT - 1),
            random.randint(0, settings.WINDOW_WIDTH - 1)
        )


class Direction(enum.Enum):

    TOP = Coordinate(-1, 0)
    DOWN = Coordinate(1, 0)
    LEFT = Coordinate(0, -1)
    RIGHT = Coordinate(0, 1)

    @classmethod
    def get_opposite_direction(cls, direction):
        return {
            cls.TOP: cls.DOWN,
            cls.DOWN: cls.TOP,
            cls.RIGHT: cls.LEFT,
            cls.LEFT: cls.RIGHT
        }[direction]

    @classmethod
    def get_random_direction(cls):
        directions = list(cls)
        return directions[random.randint(0, len(directions) - 1)]


class Bonus:

    def __init__(self, time_until_removed):
        self.time_until_removed = time_until_removed


class State:
    def __init__(self, snakes, obstacles):
        self.snakes = snakes
        self.obstacles = obstacles
        self.bonuses = dict()

    @classmethod
    def get_initial_state(cls):
        obstacles = cls.get_inital_obstacles()
        snake = cls.get_initial_snake(settings.INITIAL_SNAKE_LENGTH, obstacles)
        state = cls([snake], obstacles)

        return state

    @classmethod
    def get_inital_obstacles(cls):
        window_width = settings.WINDOW_WIDTH
        window_height = settings.WINDOW_HEIGHT

        obstacles = set()
        for i in range(window_height):
            obstacles.add(Coordinate(i, 0))
            obstacles.add(Coordinate(i, window_width - 1))

        for i in range(window_width):
            obstacles.add(Coordinate(0, i))
            obstacles.add(Coordinate(window_height - 1, i))

        return obstacles

    @classmethod
    def get_initial_snake(cls, length, obstacles):
        body = deque()

        while True:
            current_coordinate = Coordinate.get_random_coordinate()
            if current_coordinate not in obstacles:
                break

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
        if (0 <= neighbour.x < settings.WINDOW_HEIGHT)
           and (0 <= neighbour.y < settings.WINDOW_WIDTH)
           and neighbour not in body
    ]


class Snake:

    def __init__(self, body, direction, speed):
        self.body = body
        self.direction = direction
        self.speed = speed
