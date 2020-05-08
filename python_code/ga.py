from random import choice as random_choice
from engine import MoveGenerator, Game, GameController
from game_base import GAME_ROTATIONS, find_base_case


class Organism(MoveGenerator):
    def __init__(self, player_number: int, genome: str = None):
        self.PLAYER_NUMBER = player_number
        self.fitness = None

        if genome is None:
            temp = bytearray()
            with open("python_code/game-base.txt") as file:
                for line in file:
                    game = Game([int(x) for x in line.split()])
                    if not game.winner:
                        temp.append(random_choice(
                            tuple(i for i in range(9) if not game.tiles[i])))
                    else:
                        temp.append(9)
            self.genome = "".join(str(x) for x in temp)
        else:
            if len(genome) != 765:
                raise Exception("Invalid genome")
            self.genome = genome

    def move(self, game: Game):
        base_case = find_base_case(game)
        base_case_repr = f"{repr(base_case)}\n"
        game_repr = f"{repr(game)}\n"

        # print(base_case, base_case_repr, game_repr, sep="\n")

        with open("python_code/game-base.txt") as file:
            for index, line in enumerate(file):
                if line == base_case_repr:
                    base_case_move = int(self.genome[index])
                    # print(base_case_move)

                    if base_case_repr == game_repr:
                        return base_case_move

                    for rotation in GAME_ROTATIONS:
                        temp_list = []
                        for index in rotation:
                            temp_list.append(base_case.tiles[index])

                        if f"{repr(Game(temp_list))}\n" == game_repr:
                            # print(Game(temp_list))
                            for index, base_case_index in enumerate(rotation):
                                if base_case_index == base_case_move:
                                    return index

    def mutate(self):
        self.fitness = None

    def get_fitness(self):
        if self.fitness is not None:
            return self.fitness
        else:
            # TODO: fitness function
            return self.fitness

    def __repr__(self):
        return f"Organism <{self.genome}>"


if __name__ == "__main__":
    GameController(MoveGenerator(1), Organism(2), verbose=True).start()
