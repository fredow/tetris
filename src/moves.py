import numpy as np
from move import Move

class LeftMove(Move):
    CONTROL = "left"

    def get_matrice(self):
        return [0, -1]

class RightMove(Move):
    CONTROL = "right"
    def get_matrice(self):
        return [0, 1]

class DownMove(Move):
    CONTROL = "down"
    def get_matrice(self):
        return [1, 0]

'''
this is the initialization of a piec on the board, it's a move in a seense that it is spawning

we need
- y,x of the start of a piece
- the vector of the piece
- the initial state of the board
'''
class MoveOrigin(Move):
    CONTROL = "origin"
    def __init__(self, piece_shape, board_state, initial_position) -> None:
        super().__init__(piece_shape, initial_position)

        self.board_state = board_state
        print(self)

    def custom_rollback(self):
        print("bye!")

    def get_matrice(self):
        return []

class RotateMove(Move):
    CONTROL = "up"
    
    # override
    def calculate_vector(self, shape):


        rot = np.rot90(shape)

        # beef up the number of rows to make them match
        if len(rot) - len(shape) > 0:
            shape = np.vstack([shape, [0] * len(shape[0])])
        else:
            rot = np.vstack([rot, [0] * len(rot[0])])

        if len(rot[0]) - len(shape[0]) > 0:
            shape = np.column_stack([shape, [0] * len(shape)])
        else:
            rot = np.column_stack([rot, [0] * len(rot)])

        self.move_vector_command = rot - shape
        return self.move_vector_command

    def get_matrice(self):
        return []

    def rollback(self, updated_coords):
        return np.rot90(updated_coords, 3)