from random import choice as random_choice
from engine import MoveGenerator


class RandomMoveGenerator(MoveGenerator):
    def move(self, game):
        return random_choice(tuple(i for i in range(9) if not game.tiles[i]))
