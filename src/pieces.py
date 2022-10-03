from abc import ABC, abstractmethod
from dataclasses import dataclass
import random

import numpy as np

# todo: circle dependency with Piece, to type or remove, see https://stackoverflow.com/questions/7336802/how-to-avoid-circular-imports-in-python
#from board import Tile

#class Piece(ABC):
#    ...

class Block():
    parent = None
    tile = None
    def __init__(self, piece, tile) -> None:
        self.parent = piece
        self.tile = tile

class Piece(ABC):
    
    color: int
    blocks = None
    name: str
    

    def __init__(self) -> None:
        super().__init__()

        self.curr_matrice = []
        self.blocks = []


    #@abstractmethod
    #def possible_moves():
    #    ...
    def add_block(self, tile=None):
        self.blocks.append(Block(self, tile))

    def set_block_tile(self, index, tile):
        try:
            self.blocks[index].tile = tile
        except IndexError:
            print('problem')   
            

    def get_coords(self):
        return self.blocks[0].tile.get_coords()

    def rotate_base(self):
        return np.rot90(self.vector)

    def rotate(self, nb_rotation):
        self.vector = np.rot90(self.vector, nb_rotation)

    # can be used to define special movement per piece
    def get_possible_moves(self):
        return [[1, 0],[0,1],[0,-1]]


    def get_block_from_coords(self, y, x):
        for block in self.blocks:
            c = block.tile.get_coords()
            if c[0] == y and c[1] == x:
                return block 
        
        return None


    def get_matrix_from_blocks(self):
        matrice = []
        for block in self.blocks:
            matrice.append(block.tile.get_coords())

        return matrice



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

class PieceFactory():
    
    available_pieces = [Dot, Square, L, Line, Stair, Trapeze]

    def build_rand() -> Piece:
        random.seed()
        type = random.randint(0, len(PieceFactory.available_pieces) - 1)

        piece = PieceFactory.available_pieces[type]()

        # rotate the piece randomly 
        random.seed()
        rotations = random.randint(1, 4)

        #piece.rotate(rotations)
        return piece

'''
    
    def build(value: int, tile):
        
        try:
            if value == 1:
                return Square(tile)
            elif value == 3:
                return Dot(tile)
            else:
                return Joker(tile)
        except AssertionError as e:
            print(e)
    '''