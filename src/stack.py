from typing import List
from move import Move
from moves import MoveOrigin


class MoveHistory:

    history: List[Move] = None

    def __init__(self) -> None:
        self.history = []

    def push(self, move: Move):
        self.history.append(move)

    # not allowed to rollback the first move
    # stops the rollback until the piece was created
    def pop(self):
        move = self.last()
        if move and not isinstance(move, MoveOrigin):
            return self.history.pop()
        else:
            return None

    def last(self):
        if len(self.history) > 0:
            return self.history[-1]
        else:
            return None
