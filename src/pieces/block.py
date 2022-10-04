
class Block():
    parent = None
    tile = None
    def __init__(self, piece, tile) -> None:
        self.parent = piece
        self.tile = tile

    def __str__(self) -> str:
        return str(self.parent.color)