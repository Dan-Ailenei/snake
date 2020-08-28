from components import State
from logic import game_loop


def main():
    state = State.get_initial_state()

    print(state.snakes[0].body)
    game_loop(state)

main()
