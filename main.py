from components import State, draw_state
from logic import game_loop


def main():
    state = State.get_initial_state()

    print(state.snakes[0].body)
    # draw_state(state)
    game_loop(state)

main()
