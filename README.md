# Text-based Tetris 

Just playing around to brush-up my python :]
Time spent on that so far ~ 8h

## Features and roadmap

### v0.1
- ~~support left and right arrow key~~
- ~~support when game is end~~
- ~~support making a line: 3 horizon piece same value~~
- ~~support score~~
- ~~support input for variable board size~~

### v0.2
- support replay back of the game
- turn base to real time by using threads 
- make the script as an executable [pyinstaller](https://stackoverflow.com/questions/12059509/create-a-single-executable-from-a-python-project)
- add a persistance layer with adapters for files or db e.g. django/flask

### v0.x
- support playing it on the web
- extend pieces shapes
- highscores
- support multiplayer
- interactive menu with options e.g. size of board, new game, share, zooming

Technical improvements
- ~~make everything typed~~
- ~~modularize the file~~
- review OO properties grid/tile
- add linter and unit tests


## Decisions and notes
- User input library chosen: *[sshkeyboard](https://stackoverflow.com/questions/24072790/how-to-detect-key-presses/57644349#57644349)* from elimination of:
    - native input() dont support arrow key
    - keyboard() library requires root permission
    - Tkinter() requires additionnal linux installation
    - curses() requires new shell and blocks execution