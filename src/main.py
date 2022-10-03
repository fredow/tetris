
import sys
import threading
from time import sleep

import utils as utils
from game import Game


def main(args = [str]):

    
    width = None
    height = None
    if len(args) == 3 and int(args[1]) > 0 and int(args[2]) > 0:
        width = int(args[1])
        height = int(args[2])
        
    utils.clear_terminal()
    print("###############################\n#  Welcome to Tetris v0.1 :)  #\n###############################")
    input("\nPress ENTER to start the game..")
    utils.clear_terminal()

    while True:
        
        
        
        print("Get ready.")
        sleep(1)
        print("Get set...")
        sleep(1)
        print("GO!")
        sleep(1)

        game = Game(width, height)
        
        game_runner = threading.Thread(target=game.game_runner)
        game_runner.start()

        game_timer = threading.Thread(target=game.game_timer)
        game_timer.start()

        game_runner.join()
        game_timer.join()
        
        print(11111)
        
        #game_controller.join()
        print("Game done!")
        key = input("Want to play another one? Press ENTER to play again")

        if key == "y" or key == "Y" or key == "":
            continue

        break

    print("Thank you for playing :)")


if __name__ == "__main__":
    main(sys.argv) # *args