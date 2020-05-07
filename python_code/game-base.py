import logging


from engine import Game
from math import prod
from collections import deque
from copy import deepcopy


GAME_ROTATIONS = (
    (6, 3, 0, 7, 4, 1, 8, 5, 2),
    (8, 7, 6, 5, 4, 3, 2, 1, 0),
    (2, 5, 8, 1, 4, 7, 0, 3, 6),
    (6, 7, 8, 3, 4, 5, 0, 1, 2),
    (8, 5, 2, 7, 4, 1, 6, 3, 0),
    (2, 1, 0, 5, 4, 3, 8, 7, 6),
    (0, 3, 6, 1, 4, 7, 2, 5, 8)
)


def equivalent_states(game: Game):
    ret_list = []

    for rotation in GAME_ROTATIONS:
        temp_list = []
        for index in rotation:
            temp_list.append(game.tiles[index])
        ret_list.append(Game(temp_list))

    return ret_list


def sum_metric(game: Game, player: int):
    return sum(weight for tile, weight in zip(game.tiles, range(1, 10)) if tile == player)


def prod_metric(game: Game, player: int):
    return prod(weight for tile, weight in zip(game.tiles, range(1, 10)) if tile == player)


def less_state(state_one: Game, state_two: Game):
    if sum_metric(state_one, 1) == sum_metric(state_two, 1):
        if sum_metric(state_one, 2) == sum_metric(state_two, 2):
            if prod_metric(state_one, 1) == prod_metric(state_two, 1):
                if prod_metric(state_one, 2) < prod_metric(state_two, 2):
                    return state_one
                else:
                    return state_two
            else:
                if prod_metric(state_one, 1) < prod_metric(state_two, 1):
                    return state_one
                else:
                    return state_two
        else:
            if sum_metric(state_one, 2) < sum_metric(state_two, 2):
                return state_one
            else:
                return state_two
    else:
        if sum_metric(state_one, 1) < sum_metric(state_two, 1):
            return state_one
        else:
            return state_two


def find_base_case(game: Game):
    base_case = game

    for state in equivalent_states(game):
        base_case = less_state(base_case, state)

    return base_case


game_base = []


def add_to_game_base(game: Game):
    logging.basicConfig(filename="it.log", filemode="w", level=logging.DEBUG)
    base_case = find_base_case(game)
    
    if base_case.tiles not in game_base:
        game_base.append(base_case.tiles)
        logging.debug(f"{game.tiles} unique")
    else:
        logging.debug(f"{game.tiles} generic BASE_CASE={base_case}")


if __name__ == "__main__":
    inspect_queue = deque([Game()])

    while len(inspect_queue):
        game = inspect_queue.popleft()

        empty_tiles = tuple(i for i in range(9) if not game.tiles[i])

        # print(game)
        add_to_game_base(game)

        for tile in empty_tiles:
            game_copy = deepcopy(game)
            if not game.winner:
                game_copy.set_tile(tile)
                inspect_queue.append(game_copy)

    num_unique_cases = 0
    file = open("python_code/game-base.txt", "w")
    for unique_case in game_base:
        num_unique_cases += 1
        for tile in unique_case.tiles:
            file.write(tile, end="")
        file.write("\n")
    file.close()

    with open("python_code/game-base.txt", 'r+') as file:
        content = file.read()
        file.seek(0, 0)
        file.write(f"Unique_Cases: {num_unique_cases}".rstrip(
            '\r\n') + '\n' + content)

    print(f"Unique Cases: {num_unique_cases}")
