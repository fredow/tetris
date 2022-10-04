from pieces.piece import Piece


class Dot(Piece):

    def __init__(self) -> None:
        super().__init__()
        self.name = "Dot"
        self.color = 1
        for i in range(1): self.add_block()
        self.vector = [
            [1],
        ]

class Square(Piece):
  
    def __init__(self) -> None:
        super().__init__()
        self.name = "Square"
        self.color = 2
        for i in range(4): self.add_block()
        self.vector = [
            [1,1],
            [1,1]
        ]

class Line(Piece):
  
    def __init__(self) -> None:
        super().__init__()
        self.name = "Line"
        self.color = 3
        for i in range(4): self.add_block()
        self.vector = [
            [1,1,1,1],
        ]

class L(Piece):
    
    def __init__(self) -> None:
        super().__init__()
        self.color = 4
        self.name = "L"
        #self.blocks = []

        for i in range(4): self.add_block()

        self.vector = [
            [1,0,0],
            [1,1,1],
        ]


class Stair(Piece):
    
    def __init__(self) -> None:
        super().__init__()

        self.color = 5
        self.name = "Stair"
        for i in range(4): self.add_block()
        self.vector = [
            [1,1,0],
            [0,1,1],
        ]

class Trapeze(Piece):
    
    def __init__(self) -> None:
        super().__init__()

        self.color = 6
        self.name = "Trapeze"
        for i in range(4): self.add_block()
        self.vector = [
            [1,1,1],
            [0,1,0],
        ]

class Joker(Piece):
    def __init__(self) -> None:
        self.name = "Joker"
