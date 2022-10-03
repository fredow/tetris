from typing import List
from moves import MoveOrigin, LeftMove, RightMove, DownMove, RotateMove
   
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
        elif move_str == "up":
            return None
            #move = RotateMove(piece_shape, initial_position)
        else:
            return None

        padded_matrix = move.add_padding_matrix(move.piece_shape)
        
        move.calculate_vector(padded_matrix)

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