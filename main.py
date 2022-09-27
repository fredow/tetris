
'''
Features

v0.1
x- support left and right arrow key
x- support when game is end
x- support making a line: 3 horizon piece same value
x- support score
x- support input for variable board size

v0.2

Technical
todo gravy
- extend pieces shapes
- support replay back of the game
- turn base to real time by using threads 
- make the script as an executable
    https://datatofish.com/executable-pyinstaller/
- support multiplayer
- have a menu with : size of board, new game, share etc

todo optimizations
- refactor the OO properties 
x- make everything typed
x- modularize the file
- add linter and unit tests
'''

import sys

import utils
from game import Game



def main(args = [str]):

    
    width = None
    height = None
    if len(args) == 3 and int(args[1]) > 0 and int(args[2]) > 0:
        width = int(args[1])
        height = int(args[1])
        
    utils.clear_terminal()
    print("###############################\n#  Welcome to Tetris v0.1 :)  #\n###############################")
    input("\nPress any key to start the game..")
    utils.clear_terminal()

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