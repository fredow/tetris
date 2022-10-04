import os
print(os.getcwd())

import random
from pieces.piece import Piece
from pieces.piece_children import Dot, Square, L, Line, Stair, Trapeze




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
