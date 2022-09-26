
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
- support multiplayer

todo cleanup
- refactor the OO properties 
- modularize the file
'''

import random
import sys
import os

from sshkeyboard import listen_keyboard, stop_listening

class Tile:
    x = 0
    y = 0
    piece = None

    def __init__(self, y, x) -> None:
        self.x = x
        self.y = y

    def set_piece(self, p):
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

class Piece:
    value = None
    tile = None
    name = ""
    def __init__(self, v, t) -> None:
        self.value = v
        self.tile = t


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


class Board:

    
    width = 5
    height = 5
    grid = []
    def __init__(self, width, height):

        self.width = width
        self.height = height

        ui = ""
        for y in range(0, height):
            ui += "\n"
            self.grid.append([])
            for x in range(0, width):
                ui += "[" + str(y) + "," + str(x) + "]"
                self.grid[y].append(Tile(y, x))
        
        self.redraw()

    #def tile(self, id):
    #    return self.grid[id]

    def tile(self, y, x):
        
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            try:
                return self.grid[y][x]
            except IndexError:
                return None
        return None

    def validate_move(self, move):

        # validate if the board is free to move there first
        if move and move.destination and move.destination.piece is None:

            # not allowed to move up or down
            if move.destination.y == move.piece.tile.y:

                # can only move 1 case at the time
                if abs(move.destination.x - move.piece.tile.x) == 1:
                    return True


        return False

    def redraw(self, coords = False):

        ui = ""
        for y in range(len(self.grid)):
            ui += "\n"
            for x in range(len(self.grid[y])):
                if coords:
                    ui += "[" + str(y) + "," + str(x) + "]"
                else:
                    ui += str(self.tile(y,x))
        
        print(ui)


class Move:
    destination = None
    piece = None

    # to extend
    def __init__(self, p, tile) -> None:
        self.piece = p
        self.destination = tile  #tile
        pass


class Game:
    board = None
    pending_block = None
    history = []
    DEFAULT_BOARD_WIDTH = 5
    DEFAULT_BOARD_HEIGHT = 5
    input_buffer = None

    def __init__(self, width=None, height=None) -> None:
        
        if not height or not width:
            height = self.DEFAULT_BOARD_HEIGHT
            width = self.DEFAULT_BOARD_WIDTH

        self.board = Board(width, height)


    def start(self) -> None:
        print("game starting, reset timers...")


    def check_if_block_can_move(self):
        
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

    def is_game_finished(self):
        
        # check first if there is space left for new piece
        no_more_space = True
        for i in range(self.board.width):
            if self.board.tile(0, i).piece is None:
                no_more_space = False
        
        return no_more_space

    # tries to generate new piece, returns None if impossible
    def generate_new_block(self):

        if self.is_game_finished():
            return False

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
        

    def ask_user_move(self):
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

    def apply_move(self, move):

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

    def check_if_gravity_ongoing(self):
        
        tile = self.pending_block.tile
        next_destination = self.board.tile(tile.y + 1, tile.x)
        if next_destination and next_destination.piece is None:
            return True
        else:
            self.pending_block = None
            return False
        

    def apply_gravity(self):
        tile = self.pending_block.tile
        tile_destination = self.board.tile(tile.y + 1, tile.x)

        if tile_destination and tile_destination.piece is None:
            move = Move(tile.piece, tile_destination)
            self.apply_move(move)
        

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
        os.system('cls' if os.name == 'nt' else 'clear')
        self.board.redraw()
        print("Use arrows to make your move (LEFT or RIGHT) or press ENTER (or DOWN) to skip")

def main(args = []):

    # validate args
    if len(args) == 3 and int(args[1]) > 0 and int(args[2]) > 0:
        game = Game(int(args[1]), int(args[2]))
    else:
        game = Game()

    game.start()

    valid_turn = True
    while valid_turn:

        block_was_created = game.generate_new_block()

        if not block_was_created: 
            break  #game finished
        
        gravity_ongoing = True
        while gravity_ongoing:

            gravity_ongoing = game.check_if_gravity_ongoing()
            
            if gravity_ongoing:
                current_move = game.ask_user_move()

                if current_move is not None: 
                    game.apply_move(current_move)
                    game.apply_gravity() 


    print("game done !")

if __name__ == "__main__":
    print("Starting local testing!")
    main(sys.argv) 
