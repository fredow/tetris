# Text-based Tetris 

Little quick and dirty POC built in less than 24h to play around with python's OO patterns, multi-threading and matrixial arithmetic, nothing too crazy :]

Time spent on that so far ~ 20h

## Roadmap 

### v0.1
- ~~Support 1 basic shape~~
- ~~Support left and right arrow key but no rotation~~
- ~~Support when game is end~~
- ~~Support making a line: 3 horizon piece same value~~
- ~~Support score~~
- ~~Support input for variable board size~~

### v0.2 [stable]
- ~~Support replay back of the game~~
- ~~Make game real time with a timer by using threads instead of being turned-based~~
- ~~Support all pieces shapes~~
- ~~Uses matrix transformation to calculate moves instead of 2D arithmitics~~
- ~~Uses the Command design pattern to perform moves~~

### v0.3 
- Support rotation (what's remaining is to refactor the move class to use the list of coordinates instead of the origin pivot coord of the piece shape)
- Support "space" keystroke to make a piece to go directly to the bottom and spawn new piece
- Support "Tetris" scores

### v0.4
- Be able to watch a replay of a game 
- Be able to save/load a game
- Improve the screen refresh rate
- Add a persistance layer with adapters for files or db e.g. django/flask

### v0.x - long term
- Interactivity
    - Piece builder: allow the creating of custom blocks
    - Selecting size of board
    - Saving/loading/replaying games
    - Selecting speed and difficulty level
- Multiplayer
    - Collaboration one turn (piece) per person
    - Competition real-time face 2 face
    - Bot: Develop an AI to compete or collaborate with
    - Highscores
- Portability
    - Support playing it on the web with sockets
    - Make the script as an executable [pyinstaller](https://stackoverflow.com/questions/12059509/create-a-single-executable-from-a-python-project)
    - Make this run in containers


## Notes on the implementation choices
The console to listen for user input events is named *[sshkeyboard](https://stackoverflow.com/questions/24072790/how-to-detect-key-presses/57644349#57644349)*. That decision came by elimination of the following options:
    - the native input() dont support arrow keys
    - the keyboard() library requires root permission
    - the Tkinter() requires additionnal linux packages
    - the curses library requires new shell and blocks execution

We use a Command design pattern treat each user or system  move (e.g. gravity) as one isolated command that is pushed in MoveHistory's stack. Each moves can be reverted by calling move.rollback(). The rollback leverages a template pattern to allow the piece in question to add it's own custom rollback implementation

Transformations matrix where chosen instead of simple 2D table operations to create a loosly coupled interface between the move and the object entities related to the game (Board, Tile, Piece, Block). It also makes the Command pattern more cohesive as each move are tehcnically calculated vectors to apply against the state of the board. As an illustration, a "left" move would have a form of [y=0, x=-1] meaning that the vector of a piece e.g. a line such as [1,1,1,1] would have their y-axis steady, but the x (column) coordinate substracted by 1. Same concepts applies to rotations.

Multi-threading was favored over multi-processing to go for simplicity and to leverage the shared state of the Game object. We use some try-catch for cases in which the state might be inconsistant (e.g. piece just reached the bottom of the board while the user press the left arrow), in this case we would catch this and would simply ignore the user input