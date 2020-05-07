STATE_CONVERT = {
    0: "~",
    1: "X",
    2: "O",
    3: "="
}

INVERT_PLAYER = {
    1: 2,
    2: 1
}

WIN_CONDITIONS = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 4, 8),
    (2, 4, 6),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8)
)


class Game:
    def __init__(self):
        self.tiles = [0]*9
        self.winner = 0
        self.current_player = 1
        self.check_win()

    def check_win(self):
        for wincon in WIN_CONDITIONS:
            if all(self.tiles[x] == self.current_player for x in wincon):
                self.winner = self.current_player
                break
        if all(self.tiles) and not self.winner:
            self.winner = 3

    def set_tile(self, tile_number):
        if self.tiles[tile_number]:
            raise Exception("Tile already set")
        elif self.winner:
            raise Exception("Game already has a winner")
        else:
            self.tiles[tile_number] = self.current_player
        self.check_win()
        self.current_player = INVERT_PLAYER[self.current_player]

    def __str__(self):
        if self.winner:
        ret_cache = [f"Winner: {STATE_CONVERT[self.winner]}\n"]
        else:
            ret_cache = [f"Current Player: {STATE_CONVERT[self.current_player]}\n"]
        for i in range(3):
            for j in range(3):
                ret_cache.append(STATE_CONVERT[self.tiles[i*3 + j]])
            ret_cache.append("\n")
        return "".join(ret_cache)


class GameController:
    def __init__(self, x_player, o_player, verbose=True):
        self.current_game = Game()
        self.x_player = x_player
        self.o_player = o_player
        self.verbose = verbose

    def start(self):
        current_game = self.current_game
        verbose = self.verbose

        if verbose:
            print(current_game)
        while not current_game.winner:
            if current_game.current_player == 1:
                x_move = self.x_player.move(current_game)
                current_game.set_tile(x_move)
                if verbose:
                    print(current_game)  # end="")
            else:
                o_move = self.o_player.move(current_game)
                current_game.set_tile(o_move)
                if verbose:
                    print(current_game)  # end="")

        return self.current_game.winner


class MoveGenerator:
    def __init__(self, player_number):
        self.PLAYER_NUMBER = player_number

    def move(self, game):
        tile_number = input(f"{STATE_CONVERT[game.current_player]} Tile: ")
        print()
        return int(tile_number)


if __name__ == "__main__":
    controller = GameController(MoveGenerator(1), MoveGenerator(2))
    controller.start()
