
from abc import ABC, abstractmethod
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
    

    #@abstractmethod
    def custom_rollback(self):
        ...

    @abstractmethod
    def get_matrice(self) -> List[int]:
        ...

    def rollback(self):
        move_vector_command = np.array(self.move_vector_command) * -1

        reversed_state = self.apply_command(self.new_board_state, move_vector_command)

        self.destination_position = np.array(self.initial_position)
        
        # template pattern for children specific ops
        self.custom_rollback()    

        return reversed_state

    ''' applies the vector on any given matrix. 
    the vector will need to be redimensionned to fit the matrice
    its assumed that the dimensions of matrix needs to be a minimum = to the vector
    '''

    def apply_command(self, matrix, vector=None):
      
        beefedup_vector = self.resize_vector_to_match(matrix, vector)

        # update global states
        # todo: problem with rotation for the o        self.new_board_state = np.array(beefedup_vector) + np.array(matrix)        self.destination_position = np.array(self.initial_position) + self.get_matrice()
        self.new_board_state = matrix + beefedup_vector
        
        self.destination_position = np.array(self.initial_position)
        pivot_point_translation = self.get_matrice()
        if pivot_point_translation:
            self.destination_position += self.get_matrice()

        return self.new_board_state


    def undo_command(self, vector=None):

        if vector is None:
            vector = self.move_vector_command

        reversed_state = np.array(vector) - np.array(self.new_board_state)
        self.new_board_state = reversed_state
        return reversed_state

    def get_vector_coords(self):
        coords = []

        origin = self.initial_position
        if self.destination_position is not None:
            origin = self.destination_position

        for y in range(len(self.piece_shape)):
            for x in range(len(self.piece_shape[y])):
                if self.piece_shape[y][x] == 1:
                    coords.append([y + origin[0], x + origin[1]])

        return coords

    def resize_vector_to_match(self, matrix, vector_to_resize):
        piece_position = self.initial_position

        if vector_to_resize is None:
            vector_to_resize = self.move_vector_command
        if matrix is None:
            matrix = self.initial_board_state

        # beef up the calculated vector with the actual bord to be able to do ops
        # todo, need to know the more left pos, and the more right pos to fill it up dynamically, fails with rotation now
        resized_vector = vector_to_resize
        if piece_position[0] - BOARD_PADDING > 0:
            resized_vector = np.vstack([[[0] * len(resized_vector[0])] * (piece_position[0] - BOARD_PADDING), resized_vector])
        
        if len(matrix) - len(resized_vector) > 0:
            resized_vector = np.vstack([resized_vector, [[0] * len(resized_vector[0])] * (len(matrix) - len(resized_vector)) ])
        
        if piece_position[1]:
            for i in range(piece_position[1] - BOARD_PADDING): # for some reason the notation [[0] * 4] * X dont work
                resized_vector = np.column_stack([[0] * len(resized_vector), resized_vector])
            
            for i in range(len(matrix[0]) - len(resized_vector[0])): 
                resized_vector = np.column_stack([resized_vector, [0] * len(resized_vector)])
        
        return resized_vector

    def add_padding_to_matrix(self, matrix):

        # beef up matrice + 1 top and bottom and + 1 left and right
        padded_matrix = np.vstack([[[0] * len(matrix[0])], matrix])
        padded_matrix = np.vstack([padded_matrix, [[0] * len(matrix[0])]])
        
        padded_matrix = np.column_stack([[0] * len(padded_matrix), padded_matrix])
        padded_matrix = np.column_stack([padded_matrix, [0] * len(padded_matrix)])

        return padded_matrix


    # is override by moveorigine to support if len(move) = 0:
    def calculate_vector(self, matrix):

        # create transformation matrix
        move = self.get_matrice()
        
        coords = np.transpose(np.where(matrix==1))
        transformation_matrix = matrix.copy()
        transformation_matrix[np.where(transformation_matrix==1)] = 0

        # for each coords that cointain a block, apply the move 
        for point in coords:
            transformation_matrix[point[0] + move[0]][point[1] + move[1]] += 1
            transformation_matrix[point[0]][point[1]] -= 1
        
        self.move_vector_command = transformation_matrix
