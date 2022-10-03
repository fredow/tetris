from dataclasses import dataclass
from typing import List
from pieces import Block, Piece


# start introducing matrices need to review OO 

# either make the board depend on each title, and piece and moves depends on Tile
# or make everything depends on board coords and have a helper tile class to support the coords

# piece and tile are not dependent, they all relate to the main board. a piece don'T "own" a tile and a tile don't "own" a piece
    # to suppor this Move is the coordinator here
    # and removes circle dependency

@dataclass
class Tile:
    y: int = 0
    x: int = 0
    block = None

    
    TILE_STATE_OCCUPIED = 1
    TILE_STATE_EMPTY = 0
    TILE_STATE_OF_OF_BOUND = -1
    state: int = 0  

    '''
    def set_block(self, p: Piece):
        self.piece = p
        

        if self.block is not None:
            self.piece.tile = self
            self.state = self.TILE_STATE_OCCUPIED
        else:
            self.state = self.TILE_STATE_EMPTY
    '''

    def get_coords(self) -> List[int]:
        return [self.y, self.x]

    def __str__(self) -> str:
        if self.block:
            return "[" + str(self.block.parent.color) + "]"
        else:
            return "[ ]"

    def __eq__(self, other) -> bool:
        if self.x == other.x and self.y == other.y:
            return True
                
        return False



@dataclass
class Board:
    
    width: int = 5
    height: int = 5
    grid = None

    def __post_init__(self):
        self.grid = self.initialize_grid()

    # add padding for matrix operations
    def update_grid(self):
        grid = []
        for y in range(self.height + 2):
            grid.append([])
            for x in range(0, self.width + 2):
                if x != 0 and x < self.width + 1 and y != 0 and y < self.height + 1:
                    tile = Tile(y, x)
                    
                    grid[y].append(tile)
                else:
                    grid[y].append(None)

        return grid

    
    # blocks_positions[[0,1], [5,5]]
    # assyme len(blocks_positions) and nb blocks is same
    #def update_blocks_positions(self, piece: Piece, blocks_positions):
    #    for i, block in enumerate(piece.blocks):
    #        block.tile = self.tile(blocks_positions[i][0], blocks_positions[i][1])

    #    return piece.blocks


    # add padding for matrix operations
    def initialize_grid(self):
        grid = []
        for y in range(self.height + 2):
            grid.append([])
            for x in range(0, self.width + 2):
                if x != 0 and x < self.width + 1 and y != 0 and y < self.height + 1:
                    tile = Tile(y, x)
                    grid[y].append(tile)
                else:
                    grid[y].append(None)

        return grid

    def tile(self, y: int, x: int) -> Tile:
        
        if x >= 0 and x < self.width + 1 and y >= 0 and y < self.height + 1:
            try:
                return self.grid[y][x]
            except Exception as e:
                return None
        return None

    def get_matrix(self) -> List:
        matrix = []
        for y in range(len(self.grid)):
            matrix.append([])
            for x in range(len(self.grid[y])):
                t = self.grid[y][x]
                if t is None:
                    matrix[y].append(-2)
                elif isinstance(t.block, Block):
                    matrix[y].append(1)
                else:
                    matrix[y].append(0)

        return matrix

    # a number bigger then one implies 2 piece one on the other
    # a number -1 means one block is out of bounds
    def verify_state(self, matrix_to_evaluate):

        if matrix_to_evaluate is None:
            matrix_to_evaluate = self.get_matrix()

        for y in range(len(matrix_to_evaluate)):
            for x in range(len(matrix_to_evaluate[y])):
                if matrix_to_evaluate[y][x] == 2 or matrix_to_evaluate[y][x] == -1:
                    return False

        return True

    def redraw_matrix(self, grid_to_draw=None):

        if grid_to_draw is None:
            grid_to_draw = self.grid
        
        ui: str = ""
        for y in range(len(grid_to_draw)):
            for x in range(len(grid_to_draw[y])):
                t = grid_to_draw[y][x]
                if t >= 0:
                    ui += str(t)
            ui += "\n"

        print(ui)

    def redraw(self, grid_to_draw=None):

        if grid_to_draw is None:
            grid_to_draw = self.grid
        
        ui: str = ""
        for y in range(len(grid_to_draw)):
            for x in range(len(grid_to_draw[y])):
                t = self.tile(y,x)
                if t :
                    ui += str(t)
            ui += "\n"

        print(ui)
