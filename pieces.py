class Piece:
    value: int = -1
    tile = None # todo: circle dependency with Piece, to type or remove
    name: str = ""

    def __init__(self, v, t) -> None:
        self.value = v
        self.tile = t

    def __str__(self) -> str:
        raise NotImplementedError


class Joker(Piece):
    def __init__(self, v, t) -> None:
        super().__init__(v, t)

    def __str__(self) -> str:
        return "un:" + str(self.value)

class Square(Piece):
  
    def __init__(self, t) -> None:
        super().__init__(1, t)

    def __str__(self) -> str:
        return "sq:" + str(self.value)

class Triangle(Piece):
  
    def __init__(self, t) -> None:
        super().__init__(3, t)

    def __str__(self) -> str:
        return "tr:" + str(self.value)


class PieceFactory():
    
    # todo: circle dependency with Piece, to type or remove
    def build(value: int, tile):
        try:
            if value == 1:
                return Square(tile)
            elif value == 3:
                return Triangle(tile)
            else:
                return Joker(value, tile)
        except AssertionError as e:
            print(e)