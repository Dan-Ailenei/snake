import os

import settings
from components import Coordinate


def draw_snakes(snakes, current_coordinate):
    if not snakes:
        print(' ', end='')

    for snake in snakes:
        if current_coordinate not in snake.body:
            print(' ', end='')
        else:
            print('*', end='')


def draw_state(state):
    os.system('clear')
    for x in range(settings.WINDOW_HEIGHT + 1):
        for y in range(settings.WINDOW_WIDTH + 1):
            current_coordinate = Coordinate(x=x, y=y)
            if current_coordinate in state.obstacles:
                print('$', end='')
                continue

            if current_coordinate in state.bonuses:
                print(
                    state.bonuses[current_coordinate].time_until_removed, end=''
                )
                continue

            draw_snakes(state.snakes, current_coordinate)

        print()

