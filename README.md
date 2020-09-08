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
2) Download stockfish from here: https://stockfishchess.org/download/ I'v used "64-bit: Maximally compatible but slow."
3) You need to extract the exe file you downloaded and in main.py code, change the path to your stockfish engine exe file.
4) About the stockfish.set_depth(16) you can put higher values. The higher the value the more accurate the prediction
   But it's also slower. Using set depth 16 I tied against stockfish level 8 so it's preety strong as it is.
5) Run main.py before the real board is visible. After you run it wait a few seconds so the board window will pop up.
   It's getting prioritized over other windows to stay on top.
   Go to the real board and after 1 move it should start giving you predictions.
6) The program desinged to start at a fresh board. Otherwise it won't work!

# Compatibility Issues
The program is far from being perfect. It has a delay because it snap images.</br>
In order to detect pieces and it makes it vulnerable for crashing if the oppenent moved too fast.</br>
So don't even bother trying Bullet mode. It can barley handle Blitz. In long time modes like Rapid or Classical it works perfectly.
* The program only tested with Chrome on resolution 1920x1080 and the zoom needs to be 100%
* Although the program doesn't snapshot the mouse.</br> Make sure the Board window doesn't get on top of the real board.
* Technically you can make the program to work with any kind of browser on any kind of zoom.
  As long as you fix the cordinates of the board screenshot and the cell size.

# Future plans
* ~~Adding support for black pieces~~ (Added).
* ~~Saving games played~~ (Added).
* Loading game movesets from File.
* Drawing live on the board to highlight best next move.

# Disclaimer 
**This entire project done for the purpose of challenge and education.**<br>
**Not for the purpose of cheating**

**Developed on Python 3.7.7**
