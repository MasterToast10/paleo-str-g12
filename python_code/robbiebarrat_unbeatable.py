from engine import WIN_CONDITIONS, INVERT_PLAYER, Game, MoveGenerator
from random import choice as random_choice

BOARD_CORNERS = (0, 2, 6, 8)
BOARD_SIDES = (1, 3, 5, 7)

class UnbeatableMoveGenerator(MoveGenerator):
    def __init__(self, player_number: int):
        self.PLAYER_NUMBER = player_number
        self.OTHER_PLAYER = INVERT_PLAYER[player_number]
        self.turn_number = 0

    def choose_random_corner(self, tiles: list):
        return random_choice(tuple(corner for corner in BOARD_CORNERS if not tiles[corner]))

    def choose_random_side(self, tiles: list):
        return random_choice(tuple(side for side in BOARD_SIDES if not tiles[side]))

    def move(self, game: Game):
        self.turn_number += 1

        if self.turn_number == 1:
            if not game.tiles[4]:
                return 4
            else:
                return self.choose_random_corner(game.tiles)
        else:
            # Offensive
            for a, b, c in WIN_CONDITIONS:
                aT, bT, cT = [game.tiles[i] for i in (a, b, c)]
                if aT == bT == self.PLAYER_NUMBER and not cT:
                    return c
                if bT == cT == self.PLAYER_NUMBER and not aT:
                    return a
                if aT == cT == self.PLAYER_NUMBER and not bT:
                    return b
            
            # Defensive
            for a, b, c in WIN_CONDITIONS:
                aT, bT, cT = [game.tiles[i] for i in (a, b, c)]
                if aT == bT == self.OTHER_PLAYER and not cT:
                    return c
                if bT == cT == self.OTHER_PLAYER and not aT:
                    return a
                if aT == cT == self.OTHER_PLAYER and not bT:
                    return b

            # Side/Corner (Information in the original Python File by robbiebarrat)
            if self.turn_number == 2 and game.tiles[4]:
                return self.choose_random_corner(game.tiles)
            else:
                num_other_player_sides = 0
                for side in BOARD_SIDES:
                    if game.tiles[side] == self.OTHER_PLAYER:
                        num_other_player_sides += 1
                
                if num_other_player_sides >= 1 and not all(game.tiles[corner] for corner in BOARD_CORNERS):
                    return self.choose_random_corner(game.tiles)
                else:
                    if all(game.tiles[side] for side in BOARD_SIDES):
                        return self.choose_random_corner(game.tiles)
                    else:
                        return self.choose_random_side(game.tiles)
