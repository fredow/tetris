from typing import List
from dataclasses import dataclass
from move import Move


class MoveHistory:

    history: List[Move] = None

    def __init__(self) -> None:
        self.history = []

    def push(self, move: Move):
        self.history.append(move)

    # not allowed to rollback the first move
    # todo: should also forbid this for every new piece
    def pop(self):
        if len(self.history) > 1: 
            return self.history.pop()
        else:
            return None

    def last(self):
        if len(self.history) > 0:
            return self.history[-1]
        else:
            return None
