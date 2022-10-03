# native libraries
import copy
import random
from time import sleep
from typing import List

# installed libraries
from sshkeyboard import listen_keyboard, stop_listening

# app dependencies
from pieces import Piece, PieceFactory
from board import Board
from move import Move, MoveFactory
import numpy as np
import utils

BUFFER = 1
class Game:
    board: Board = None
    pending_piece: Piece = None
    history: List[Move] = []
    DEFAULT_BOARD_WIDTH: int = 10
    DEFAULT_BOARD_HEIGHT: int = 22
    input_buffer: str = ""
    score: int = 0

    def __init__(self, width: int = DEFAULT_BOARD_WIDTH, height: int = DEFAULT_BOARD_HEIGHT) -> None:
        
        if not height or not width:
            height = self.DEFAULT_BOARD_HEIGHT
            width = self.DEFAULT_BOARD_WIDTH

            # or randomize it...

        # initialized defaults because of python mutable default behaviour
        self.history = []
        self.pending_piece = None
        self.score = 0
        self.board = Board(width, height)


    def start(self) -> None:
        print("Get ready.")
        sleep(1)
        print("Get set...")
        sleep(1)
        print("GO!")
        sleep(1)

        game_ongoing = True
        while game_ongoing:

            success = self.generate_new_block()
            
            if not success: break
            gravity_ongoing = self.check_if_gravity_ongoing()

            while gravity_ongoing:

                user_move = self.ask_user_move()

                if isinstance(user_move, Move): 

                    gravity_ongoing = self.check_if_gravity_ongoing(apply_if_possible=True)


            # apply score
            self.evaluate_score(self.history[-1])

            # check if game finish
            game_ongoing = not self.is_game_finished()
            if not game_ongoing:
                print("ending")

    
    # take the last move played, and check if there is some points
    # if so, remove the full line and make blocks fall
    def evaluate_score(self, move: Move):
        if move.destination_position is None:
            row_to_evaluate: int = len(move.piece_shape) - 1
        else:
            row_to_evaluate: int = move.destination_position[0] + len(move.piece_shape) - 1

        row_filled: bool = True
        for i in range(BUFFER, self.board.width):
            tile = self.board.tile(row_to_evaluate, i)
            if tile and tile.block is None:
                row_filled = False
                break

        
        if row_filled:
            self.score += self.pending_piece.color

            # O(N) instead of O(n2) by this trick, todo: would work if it was not objects
            #top_line = [0] * self.board.width
            #new_arr = [top_line] + self.board.grid[0:-1]
            #self.board.grid = new_arr
            
            for x in range(BUFFER, self.board.width + BUFFER):
                t = self.board.tile(row_to_evaluate, x)
                if t is not None:
                    if t.block is not None:
                        del t.block
                        t.block = None

            # move all the piece down 1 row, delete the last row pieces and initialize the first row
            if row_to_evaluate > 0:
                for y in range(row_to_evaluate, BUFFER, -1):
                    for x in range(BUFFER, self.board.width + BUFFER):
                        self.board.tile(y, x).block = self.board.tile(y - 1, x).block                


    def is_game_finished(self) -> bool:
        
        # check if the row 0 (top) contains one piece, if yes then it's over
        game_over = False
        for i in range(self.board.width):
            t = self.board.tile(BUFFER, i)
            if t and t.block is not None:
                game_over = True
        
        return game_over

    '''
    generates a random piece at (0,0)
    randomly move it on the x axis
    if the move is illigale it means the game is done
    '''
    def generate_new_block(self):

        #todo: will force a gap of 4 from the right which for the square will never allow it to be at the boarder
        random.seed()
        pos_x = random.randint(BUFFER, self.board.width - 5) 
        matrix = self.board.get_matrix()
        self.pending_piece = PieceFactory.build_rand()
        
        move = MoveFactory.build_first(
            self.pending_piece.vector,
            matrix, [1, pos_x]
        )

        # align the piece matrix with the random new position
        valid = self.board.verify_state(move.new_board_state)

        if valid:
            self.commit_and_redraw(move)
            
        self.redraw()
        return valid


    def ask_user_move(self) -> Move:
        move: Move = None

        def ask_user_move_callback(key):
            self.input_buffer = key
            stop_listening()
        
        played: bool = False
        while not played:    
            listen_keyboard(on_press=ask_user_move_callback)

            # special case: revert
            if self.input_buffer == "backspace" and len(self.history) > 1:
                move = self.history[-1]
                move.rollback()
                self.commit_and_redraw(move, pop=True)
            else:
                current_piece_coords = self.pending_piece.get_matrix_from_blocks()
                move = MoveFactory.build(
                        self.input_buffer,
                        self.pending_piece.vector,
                        current_piece_coords[0])

                if not isinstance(move, Move):
                    print("Command '" + self.input_buffer  + "'not supported, maybe in v2!")
                    continue

                # now try to apply the move and check if board is in a valid state
                move.apply_command(self.board.get_matrix())
                valid = self.board.verify_state(move.new_board_state)

                if valid:
                    self.commit_and_redraw(move)
                    return move
                else:
                    print("Out of bound! Nice try...")


                
    def commit_and_redraw(self, move: Move, pop=False):
        
        for b in self.pending_piece.blocks:
            if b.tile is not None: b.tile.block = None

        coords = move.get_vector_coords()
        for i, c in enumerate(coords):
            tile = self.board.tile(c[0], c[1])
            self.pending_piece.blocks[i].tile = tile
            tile.block = self.pending_piece.blocks[i]
    
        if pop is True:
            self.history.pop()
        else:
            self.history.append(move)

        self.redraw()

    def check_if_gravity_ongoing(self, apply_if_possible = False) -> bool:
        
        g = MoveFactory.build(
            "down", 
            self.pending_piece.vector,
            self.pending_piece.get_matrix_from_blocks()[0]
        )

        current_state = self.board.get_matrix()
        g.apply_command(current_state)

        is_valid = self.board.verify_state(g.new_board_state)

        if apply_if_possible and is_valid:
            self.commit_and_redraw(g)

            return self.check_if_gravity_ongoing()
        else:
            return is_valid


    def apply_gravity(self) -> Move:
        tile = self.pending_piece.tile
        tile_destination = self.board.tile(tile.y + 1, tile.x)

        move = None
        if tile_destination and tile_destination.piece is None:
            move = Move(tile.piece, tile_destination)
            self.apply_move(move)
        
        return move

    def redraw(self):
        utils.clear_terminal()
        print("Score: " + str(self.score))
        self.board.redraw()
        print("Instructions:  \n- Press LEFT or RIGHT to move. \n- Press ENTER or DOWN) to skip. \n- Press BACKSPACE to rollback")