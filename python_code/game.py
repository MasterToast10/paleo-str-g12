from engine import GameController, MoveGenerator
from rmg import RandomMoveGenerator


controller = GameController(RandomMoveGenerator(), MoveGenerator())
if the_winner := controller.start() < 3:
    print(f"Player {the_winner} won!")
else:
    print("Draw!")
