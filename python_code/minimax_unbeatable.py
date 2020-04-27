from copy import deepcopy

from engine import INVERT_PLAYER, MoveGenerator, Game

def evaluate_game_state(the_game: Game, the_player: int):
    if the_game.winner == the_player:
        return +10
    elif the_game.winner == INVERT_PLAYER[the_player]:
        return -10
    else:
        return 0

def minimax(the_game: Game, the_player: int, depth: int, is_maximizer: bool):
    score = evaluate_game_state(the_game, the_player)

    # If someone won return the evaluated score
    if score:
        return score

    # If nobody won but game ended (i.e. tie) return 0
    if the_game.winner:
        return 0

    # If maximizer move
    if is_maximizer:
        best = -1000

        for tile, tile_number in zip(the_game.tiles, range(9)):
            # If tile is empty
            if not tile:
                game_copy = deepcopy(the_game)
                game_copy.set_tile(tile_number)
                best = max(best, minimax(game_copy, INVERT_PLAYER[the_player], depth + 1, False))

        return best
    else:
        best = 1000

        for tile, tile_number in zip(the_game.tiles, range(9)):
            #If tile is empty
            if not tile:
                game_copy = deepcopy(the_game)
                game_copy.set_tile(tile_number)
                best = min(best, minimax(game_copy, INVERT_PLAYER[the_player], depth + 1, True))

        return best
    
def find_best_move(the_game: Game, the_player: int):
    best_val = -1000
    best_move = -1

    for tile, tile_number in zip(the_game.tiles, range(9)):
        if not tile:
            game_copy = deepcopy(the_game)
            if the_player == the_game.current_player:
                raise Exception("Player is not current player")
            game_copy.set_tile(tile_number)

            move_val = minimax(game_copy, INVERT_PLAYER[the_player], 0, False)

            if move_val > best_val:
                best_move = tile_number
                best_val = move_val

    return best_move

class UnbeatableMoveGenerator(MoveGenerator):
    def move(self, game):
        return find_best_move(game, INVERT_PLAYER[self.PLAYER_NUMBER])

if __name__ == "__main__":
    game = Game()
    # print(find_best_move(game, 1))
    game = Game()
    game.set_tile(0)
    game.set_tile(1)
    game.set_tile(2)
    game.set_tile(3)
    game.set_tile(5)
    game.set_tile(4)
    print(find_best_move(game, 2))
    # print(evaluate_game_state(game, 2))
    # print(evaluate_game_state(Game([2, 2, 2, 0, 0, 0, 0, 0, 0]), 1))