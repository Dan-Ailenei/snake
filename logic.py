import random
import time
from functools import reduce

from components import Direction, State, Bonus, Coordinate
from graphics import draw_state
from khbit import KBHit
from settings import (
    DELTA_USER_INPUT, BONUS_INSERT_TIME,
    BONUS_LIVE_TIME_RANGE, INITIAL_SNAKE_LENGTH)


CONTROL_KEYS = {
    'w': Direction.TOP,
    's': Direction.DOWN,
    'd': Direction.RIGHT,
    'a': Direction.LEFT,
}


def is_dead(snake, state):
    snake_head = snake.body.pop()
    snakes_bodies = reduce(
        lambda x, y: x | y, [set(snake.body) for snake in state.snakes]
    )
    if snake_head in (state.obstacles | snakes_bodies):
        snake.body.append(snake_head)
        return True

    snake.body.append(snake_head)
    return False


def advance_snakes(state: State):
    for snake in state.snakes:
        snake.body.append(snake.body[-1] + snake.direction.value)

        snake_head = snake.body[-1]
        if snake_head not in state.bonuses:
            snake.body.popleft()
        else:
            state.bonuses.pop(snake_head)

    dead_snakes_positions = []
    for i, snake in enumerate(state.snakes):
        if is_dead(snake, state):
            state.obstacles.update(snake.body)
            dead_snakes_positions.append(i)

    for dead_snake in dead_snakes_positions:
        state.snakes.pop(dead_snake)
        state.snakes.append(
            state.get_initial_snake(INITIAL_SNAKE_LENGTH, state.obstacles)
        )


def handle_bonuses(state: State, loop_count):
    for coordinate, bonus in dict(state.bonuses).items():
        bonus.time_until_removed -= 1
        if bonus.time_until_removed == 0:
            state.bonuses.pop(coordinate)

    if loop_count % BONUS_INSERT_TIME == 0:
        state.bonuses[Coordinate.get_random_coordinate()] = (
            Bonus(time_until_removed=random.randint(*BONUS_LIVE_TIME_RANGE))
        )


def game_loop(state):
    kb = KBHit()

    draw_state(state)
    loop_count = 0
    while True:
        time.sleep(DELTA_USER_INPUT)
        if kb.kbhit():
            user_input_char = kb.getch()
            user_input_direction = CONTROL_KEYS.get(user_input_char.lower())

            if (user_input_direction != (
                Direction.get_opposite_direction(state.snakes[0].direction))
                and user_input_direction is not None
            ):
                state.snakes[0].direction = user_input_direction

        advance_snakes(state)
        loop_count += 1

        handle_bonuses(state, loop_count)
        draw_state(state)

    kb.set_normal_term()
