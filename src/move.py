
from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
from typing import List

BOARD_PADDING = 1

# must be serializable and the most decoupled
#@dataclass
class Move (ABC):
    
    # inputs
    piece_shape: List # represent the piece shape in isolation (without board)
    initial_position = [int] # reference the 0,0 of the piece in relation of the board
    
    # outputs 
    initial_board_state: None
    move_vector_command = None

    # reusable states across the system
    new_board_state = None
    destination_position = None
    

    def __init__(self, piece_shape, initial_position) -> None:
        super().__init__()
        self.piece_shape = piece_shape
        self.initial_board_state = []
        self.initial_position = initial_position
        self.move_vector_command = None
        self.new_board_state = None
        self.destination_position = None
    


    @abstractmethod
    def get_matrice(self) -> List[int]:
        ...

    def rollback(self):
        move_vector_command = np.array(self.move_vector_command) * -1

        reversed_state = self.apply_command(self.new_board_state, move_vector_command)

        self.destination_position = np.array(self.initial_position)

        return reversed_state

    ''' applies the vector on any given matrix. 
    the vector will need to be redimensionned to fit the matrice
    its assumed that the dimensions of matrix needs to be a minimum = to the vector
    '''
    def apply_command_first(self, matrix):
        if matrix is None:
            matrix = self.initial_board_state

        self.new_board_state = np.array(self.move_vector_command) + np.array(matrix)
        return self.new_board_state

    def apply_command(self, matrix, vector=None):
        piece_position = self.initial_position

        if vector is None:
            vector = self.move_vector_command
        if matrix is None:
            matrix = self.initial_board_state

        # beef up the calculated vector with the actual bord to be able to do ops
        beefedup_vector = vector
        if piece_position[0] - BOARD_PADDING > 0:
            beefedup_vector = np.vstack([[[0] * len(beefedup_vector[0])] * (piece_position[0] - BOARD_PADDING), beefedup_vector])
        
        if len(matrix) - len(beefedup_vector) > 0:
            beefedup_vector = np.vstack([beefedup_vector, [[0] * len(beefedup_vector[0])] * (len(matrix) - len(beefedup_vector)) ])
        
        if piece_position[1]:
            for i in range(piece_position[1] - BOARD_PADDING): # for some reason the notation [[0] * 4] * X dont work
                beefedup_vector = np.column_stack([[0] * len(beefedup_vector), beefedup_vector])
            
            for i in range(len(matrix[0]) - len(beefedup_vector[0])): 
                beefedup_vector = np.column_stack([beefedup_vector, [0] * len(beefedup_vector)])
        
        # update global states
        # todo: problem with rotation for the origin?
        self.new_board_state = np.array(beefedup_vector) + np.array(matrix)
        self.destination_position = np.array(self.initial_position) + self.get_matrice()
        


        return self.new_board_state

    def undo_command(self, vector=None):

        if vector is None:
            vector = self.move_vector_command

        reversed_state = np.array(vector) - np.array(self.new_board_state)
        self.new_board_state = reversed_state
        return reversed_state

    def get_vector_coords(self, new_position=False):
        coords = []

        origin = self.initial_position
        if self.destination_position is not None:
            origin = self.destination_position

        for y in range(len(self.piece_shape)):
            for x in range(len(self.piece_shape[y])):
                if self.piece_shape[y][x] == 1:
                    coords.append([y + origin[0], x + origin[1]])

        return coords

    '''
    need the piece vector
    
    
    '''
    def calculate_vector(self):

        y_len = len(self.piece_shape)
        x_len = len(self.piece_shape[0])

        move = self.get_matrice()

        # beef up matrice + 1 top and bottom and + 1 left and right
        beefed_upmatrix = np.vstack([[[0] * x_len], self.piece_shape])
        beefed_upmatrix = np.vstack([beefed_upmatrix, [[0] * x_len]])
        
        beefed_upmatrix = np.column_stack([[0] * len(beefed_upmatrix), beefed_upmatrix])
        beefed_upmatrix = np.column_stack([beefed_upmatrix, [0] * len(beefed_upmatrix)])

        # create transformation matrix
        coords = np.transpose(np.where(beefed_upmatrix==1))
        transformation_matrix = beefed_upmatrix.copy()
        transformation_matrix[np.where(transformation_matrix==1)] = 0

        # for each coords that cointain a block, apply the move 
        
        for point in coords:
            transformation_matrix[point[0] + move[0]][point[1] + move[1]] += 1
            transformation_matrix[point[0]][point[1]] -= 1
        # apply
        
        self.move_vector_command = transformation_matrix
        #print(self.move_vector_command)


    #fill the matrix based to match it with an existing one
    def calculate_vector_first(self):

        y_len = len(self.piece_shape)
        x_len = len(self.piece_shape[0])

        BUFFER = 1
        nb_to_append_y = len(self.board_state) - y_len - self.initial_position[0]# - BUFFER
        nb_to_append_x = len(self.board_state[0]) - x_len# - BUFFER

        extended_matrix = np.vstack([[[0] * x_len] * self.initial_position[0], self.piece_shape])
        extended_matrix = np.vstack([extended_matrix, [[0] * x_len] * nb_to_append_y])
        
        nb_columns_added = 0
        for i in range(0, self.initial_position[1]):
            if nb_columns_added < nb_to_append_x:
                extended_matrix = np.column_stack([[0] * len(self.board_state), extended_matrix])
                nb_columns_added += 1

        # extend on the right for the remainings
        for i in range(nb_to_append_x - nb_columns_added):
            extended_matrix = np.column_stack([extended_matrix, [0] * len(self.board_state)])

        self.move_vector_command = extended_matrix


class LeftMove(Move):
    def get_matrice(self):
        return [0, -1]

class RightMove(Move):
    def get_matrice(self):
        return [0, 1]

class DownMove(Move):
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

    def __init__(self, piece_shape, board_state, initial_position) -> None:
        super().__init__(piece_shape, initial_position)

        self.board_state = board_state
        print(self)

    def get_matrice(self):
        return []

class RotateMove(Move):

    # special case
    def get_matrice(self):
        return [] 


    def apply(self) -> bool:
        return np.rot90(self.curr_matrice)

    def rollback(self, updated_coords):
        return np.rot90(updated_coords, 3)

   
'''
we need 
- the vector of the piece and its 0,0 or a list of its coords
- current map
- vector to appply

we process it by
- trasfoming the 0----0 -> 00---- 
- appling 


'''
class MoveFactory():
    def build(move_str: str, piece_shape: List, initial_position):
    
        move = None
        if move_str == "left":
            move = LeftMove(piece_shape, initial_position)
        elif move_str == "right":
            move = RightMove(piece_shape, initial_position)
        elif move_str in ["enter", "esc", "down"]:
            move = DownMove(piece_shape, initial_position) 
        else:
            return None

        move.calculate_vector()

        return move

    def build_first(piece_shape: List, state: List, initial_position: List[int]):
        
        move = MoveOrigin(piece_shape, state, initial_position)
        move.calculate_vector_first()
        move.apply_command_first(state)

        return move

        '''try:
            for m in MoveFactory.possible_moves:
                if m.matrice == matrice:
                    return m()
        except AssertionError as e:
            print(e)
        '''