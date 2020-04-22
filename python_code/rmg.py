from random import choice
from engine import MoveGenerator


class RandomMoveGenerator(MoveGenerator):
    def move(self, game):
        return choice(tuple(i for i in range(9) if not game.tiles[i]))
