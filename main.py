
'''
todo core
x- support left and right arrow key
x- support when game is end
- support making a line: 3 horizon piece same value
- support score
x- support input for variable board size

todo gravy
- extend pieces shapes
- support replay back of the game
- turn base to real time by using threads 
- make the script as an executable
    https://datatofish.com/executable-pyinstaller/
- support multiplayer
- have a menu with : size of board, new game, share etc
- show timer in real time

todo optimizations
- refactor the OO properties 
x- make everything typed
- modularize the file
- add linter and unit tests
'''

import random
import sys
import os
from time import sleep
from typing import List
from sshkeyboard import listen_keyboard, stop_listening

class Piece:
    value: int = -1
    tile = None #can't type it now, need to split in files and import before
    name: str = ""

    def __init__(self, v, t) -> None:
        self.value = v
        self.tile = t

    def __str__(self) -> str:
        raise NotImplementedError

class Tile:
    x: int = 0
    y: int = 0
    piece = None

    def __init__(self, y: int, x: int) -> None:
        self.x = x
        self.y = y
        self.piece = None

    def set_piece(self, p: Piece):
        self.piece = p

        if self.piece is not None:
            self.piece.tile = self


    def __str__(self) -> str:
        if self.piece:
            return "[" + str(self.piece.value) + "]"
        else:
            return "[ ]"

    def __eq__(self, other) -> bool:
        if self.x == other.x and self.y == other.y:
            return True
                
        return False


class TBD(Piece):
    def __init__(self, v, t) -> None:
        super().__init__(v, t)

    def __str__(self) -> str:
        return "un:" + str(self.value)

class Square(Piece):
  
    def __init__(self, t) -> None:
        super().__init__(1, t)

    def __str__(self) -> str:
        return "sq:" + str(self.value)

class Move:
    destination: Tile = None
    piece: Piece = None

    # to extend
    def __init__(self, p, tile) -> None:
        self.piece = p
        self.destination = tile
        pass


class Board:
    
    width: int = 5
    height: int = 5
    grid: List = [int]

    def __init__(self, width: int, height: int):

        self.width = width
        self.height = height

        # mutable default
        self.grid = []

        for y in range(height):
            self.grid.append([])
            for x in range(0, width):
                self.grid[y].append(Tile(y, x))
        

    def tile(self, y: int, x: int) -> Tile:
        
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            try:
                return self.grid[y][x]
            except IndexError:
                return None
        return None

    def validate_move(self, move: Move) -> bool:

        # validate if the board is free to move there first
        if move and move.destination and move.destination.piece is None:

            # not allowed to move up or down
            if move.destination.y == move.piece.tile.y:

                # can only move 1 case at the time
                if abs(move.destination.x - move.piece.tile.x) == 1:
                    return True


        return False

    def redraw(self, coords = False):

        ui: str = ""
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if coords:
                    ui += "[" + str(y) + "," + str(x) + "]"
                else:
                    ui += str(self.tile(y,x))
            ui += "\n"
        print(ui)


class Game:
    board: List = None
    pending_block: Piece = None
    history: List = [Move]
    DEFAULT_BOARD_WIDTH: int = 5
    DEFAULT_BOARD_HEIGHT: int = 5
    input_buffer: str = ""
    score: int = 0

    def __init__(self, width: int = DEFAULT_BOARD_WIDTH, height: int = DEFAULT_BOARD_HEIGHT) -> None:
        
        if not height or not width:
            height = self.DEFAULT_BOARD_HEIGHT
            width = self.DEFAULT_BOARD_WIDTH

            # or randomize it...

        # initialized defaults because of python mutable default behaviour
        self.history = []
        self.pending_block = None
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

            self.generate_new_block()
            
            gravity_ongoing = True
            while gravity_ongoing:

                gravity_ongoing = self.check_if_gravity_ongoing()
                
                if gravity_ongoing:
                    user_move = self.ask_user_move()

                    if user_move is not None: 
                        self.apply_move(user_move)
                        self.apply_gravity() 

                else:

                    # apply score
                    self.evaluate_score(self.history[-1])

                    # check if game finish
                    game_ongoing = not self.is_game_finished()

    
    # take the last move played, and check if there is some points
    # if so, remove the full line and make blocks fall
    def evaluate_score(self, move: Move):
        row_to_evaluate: int = move.destination.y

        row_filled: bool = True
        for i in range(self.board.width):
            tile = self.board.tile(row_to_evaluate, i)
            if tile and tile.piece is None:
                row_filled = False
                break

        
        if row_filled:
            self.score += self.board.width

            # O(N) instead of O(n2) by this trick, todo: would work if it was not objects
            #top_line = [0] * self.board.width
            #new_arr = [top_line] + self.board.grid[0:-1]
            #self.board.grid = new_arr

            # move all the piece down 1 row, delete the last row pieces and initialize the first row
            for y in range(self.board.height -1, -1, -1):
                for x in range(self.board.width):
                    if row_to_evaluate == y:
                        del self.board.tile(y, x).piece

                    if y == 0:
                        self.board.tile(y, x).piece = None
                    else:
                        self.board.tile(y, x).piece = self.board.tile(y - 1, x).piece                

    def check_if_block_can_move(self) -> bool:
        
        tile = self.pending_block.tile

        # generate possible moves
        possible_moves = [
            self.board.tile(tile.y, tile.x - 1),
            self.board.tile(tile.y, tile.x + 1),
            self.board.tile(tile.y + 1, tile.x)
        ]

        current_piece_can_move = False
        for destination in possible_moves:

            if destination and destination.piece is None:
                current_piece_can_move = True
        
        return current_piece_can_move

    def is_game_finished(self) -> bool:
        
        # check if the row 0 (top) contains one piece, if yes then it's over
        game_over = False
        for i in range(self.board.width):
            if self.board.tile(0, i).piece is not None:
                game_over = True
        
        return game_over

    # tries to generate new piece, returns None if impossible
    def generate_new_block(self):

        # generate a piece
        random.seed()
        r = random.randint(1, 4)

        # generate a random position from the top
        pos = -1
        attempts = 0
        while pos == -1 and attempts < 100:
            pos = random.randint(0, self.board.width - 1)

            if self.board.tile(0, pos).piece is not None:
                pos = -1
                attempts += 1

        if r == 1:
            piece = Square(self.board.tile(0, pos))
        else:
            piece = TBD(r, self.board.tile(0, pos)) #y, x

        self.board.tile(0, pos).set_piece(piece)

        self.pending_block = piece
        if self.pending_block is None:
            print("new block " + str(piece))

        self.redraw()
        return True

    #def ask_user_move_callback(self, key):
        

    def ask_user_move(self) -> Move:
        move = None

        def ask_user_move_callback(key):
            self.input_buffer = key
            stop_listening()
        
        while not move:    
            listen_keyboard(on_press=ask_user_move_callback)

            if self.input_buffer in ["l", "left"]:
                new_x = self.pending_block.tile.x + -1
                new_y = self.pending_block.tile.y + 0
            elif self.input_buffer in ["r", "right"]:
                new_x = self.pending_block.tile.x + 1
                new_y = self.pending_block.tile.y + 0
            elif self.input_buffer in ["enter", "esc", "down"]:
                return Move(self.pending_block, self.pending_block.tile)
            else:
                continue
                    
            
            move_to_validate = Move(self.pending_block, self.board.tile(new_y, new_x))
            if self.board.validate_move(move_to_validate):
                move = move_to_validate

        return move

    def apply_move(self, move: Move):

        # make change on the board here
        if move.destination.y != move.piece.tile.y or move.destination.x != move.piece.tile.x:
            
            x = move.piece.tile.x
            y = move.piece.tile.y
            self.board.tile(move.destination.y, move.destination.x).set_piece(move.piece)
            self.board.tile(y, x).set_piece(None)
            self.pending_block = move.piece

            if self.pending_block is None:
                print(move)
            self.history.append(move)
            self.redraw()

    def check_if_gravity_ongoing(self) -> bool:
        
        tile = self.pending_block.tile
        next_destination = self.board.tile(tile.y + 1, tile.x)
        if next_destination and next_destination.piece is None:
            return True
        else:
            self.pending_block = None
            return False
        

    def apply_gravity(self) -> Move:
        tile = self.pending_block.tile
        tile_destination = self.board.tile(tile.y + 1, tile.x)

        move = None
        if tile_destination and tile_destination.piece is None:
            move = Move(tile.piece, tile_destination)
            self.apply_move(move)
        
        return move

    def apply_gravity_all(self):

        tile_applied_gravity = []
        for y in range(len(self.board.grid)):
            for x in range(len(self.board.grid[y])):
                tile = self.board.tile(y, x)
                tile_destination = self.board.tile(y + 1, x)
                if tile and tile.piece is not None and tile_destination and tile_destination.piece is None:
                    
                    if not tile in tile_applied_gravity:
                        move = Move(tile.piece, tile_destination)
                        tile_applied_gravity.append(tile_destination)
                        print("Gravity for " + str(y) + "," + str(x))
                        self.apply_move(move)
                        


    def redraw(self):
        clear_terminal()
        print("Score: " + str(self.score))
        self.board.redraw()
        print("Use arrows to make your move (LEFT or RIGHT) or press ENTER (or DOWN) to skip")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def main(args = [str]):

    
    width = None
    height = None
    if len(args) == 3 and int(args[1]) > 0 and int(args[2]) > 0:
        width = int(args[1])
        height = int(args[1])
        
    clear_terminal()
    print("###############################\n#  Welcome to Tetris v0.1 :)  #\n###############################")
    input("\nPress any key to start the game..")
    clear_terminal()

    while True:
        game = Game(width, height)
        game.start()
        
        print("Game done!")
        key = input("Want to play another one? (Y/n) ")

        if key == "y" or key == "Y" or key == "":
            continue

        break

    print("Thank you for playing :)")


if __name__ == "__main__":
    main(sys.argv) # *args