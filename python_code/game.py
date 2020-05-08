from engine import GameController, MoveGenerator
from rmg import RandomMoveGenerator
from robbiebarrat_unbeatable import UnbeatableMoveGenerator
from ga import Organism


def playGame(move_generator_x: MoveGenerator, move_generator_o: MoveGenerator, verbose=True):
    return GameController(move_generator_x(1), move_generator_o(2), verbose).start()


if __name__ == "__main__":
    counters = [0, 0, 0]

    for i in range(10):
        the_winner = playGame(RandomMoveGenerator,
                              Organism, verbose=True)

        counters[the_winner - 1] += 1

        # if the_winner < 3:
        #     print(f"Player {the_winner} won!")
        # else:
        #     print("Draw!")

    print(f"X: {counters[0]}\nO: {counters[1]}\nDraw: {counters[2]}")
