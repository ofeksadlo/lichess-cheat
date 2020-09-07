# Lichess-Cheat
Simple chess cheat for lichess based on opencv.
#
![Showcase](https://raw.githubusercontent.com/ofeksadlo/lichess-cheat/master/showcase.gif)

# What it does
Creates a new board window which shows you the best next move. For
you and your opponent.

# How it works?
The program captures every 501 milliseconds the board. And then loops through every cell
to detect if a piece moved. If a piece moved it append to the game moveset. Then the program
will feed the stockfish engine with the game movesets in order to get the best next move.

The method is quite easy actually. In order to get prediction for next moves we need to detect which pieces already moved.
In lichess site it's done by drawing the green color around the cell. So we need to detect 2 specific cells.
One green cell without a piece in it (Where the piece moved from) and one green cell with a piece in it (Where the piece moved to).
The detection is done by color matching.
Now we have the last moveset and we can feed are stockfish engine to get predictions.

# How to make it work
1) Download the main.py and the data folder
2) Download stockfish from here: https://stockfishchess.org/download/ I'v used 64-bit: Maximally compatible but slow.
3) You need to extract the exe file you downloaded and in main.py code, change the path to your stockfish engine exe file.
4) About the stockfish.set_depth(16) you can put higher values. The higher the value the more accurate the prediction
   But it's also slower. Using set depth 16 I tied against stockfish level 8 so it's preety strong as it is.
5) You can go a head and run it for now it only work for white pieces. But soon it will work for black pieces as well.
   After you run it wait a few seconds so the board window will pop up. It's getting prioritized over other window to stay on top.
   Now go a head and start a game and in the board window it will give you next best move.

# Compatibility Issues
* The program only tested on Chrome and the zoom needs to be 100%
* Although the program doesn't snapshot the mouse. Make sure the Board window doesn't get on top of the real board.
* Technically you can use the program work with any kind of browser on any kind of zoom.
  As long as you fix the cordinates of the board screenshot.
