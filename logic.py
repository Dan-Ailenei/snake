import time

import getch

from components import Direction, draw_state
from khbit import KBHit
from settings import DELTA_USER_INPUT

arrow_chars = {
    'w': Direction.TOP,
    's': Direction.DOWN,
    'd': Direction.RIGHT,
    'a': Direction.LEFT,
}

oppos_direction = {
    Direction.TOP: Direction.DOWN,
    Direction.DOWN: Direction.TOP,
    Direction.RIGHT: Direction.LEFT,
    Direction.LEFT: Direction.RIGHT,

}


def advance_snakes(snakes):
    for snake in snakes:
        snake.body.append(snake.body[-1] + snake.direction.value)
        snake.body.popleft()


def game_loop(inital_state):
    kb = KBHit()

    draw_state(inital_state)
    while True:
        time.sleep(DELTA_USER_INPUT)
        if kb.kbhit():
            c = kb.getch()
            user_input_direction = arrow_chars.get(c.lower())

            if user_input_direction != oppos_direction[inital_state.snakes[0].direction]:
                inital_state.snakes[0].direction = user_input_direction

        advance_snakes(inital_state.snakes)
        draw_state(inital_state)

    kb.set_normal_term()

# game_loop(None)