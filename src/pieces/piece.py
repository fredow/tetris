from abc import ABC, abstractmethod
import numpy as np

from pieces.block import Block

# todo: circle dependency with Piece, to type or remove, see https://stackoverflow.com/questions/7336802/how-to-avoid-circular-imports-in-python
#from board import Tile

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
            if block.tile is not None:
                matrice.append(block.tile.get_coords())
            else:
                print("Piece ghost")

        return matrice

