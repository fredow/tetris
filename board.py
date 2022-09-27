from typing import List
from pieces import Piece


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
