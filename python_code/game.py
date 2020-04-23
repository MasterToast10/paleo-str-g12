from engine import GameController, MoveGenerator
from rmg import RandomMoveGenerator
from unbeatable import UnbeatableMoveGenerator

controller = GameController(RandomMoveGenerator(1), UnbeatableMoveGenerator(2))
if (the_winner := controller.start()) < 3:
    print(f"Player {the_winner} won!")
else:
    print("Draw!")
