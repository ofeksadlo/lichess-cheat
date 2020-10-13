# Lichess-Cheat
Simple chess cheat for lichess based on opencv.
#
![Showcase](https://raw.githubusercontent.com/ofeksadlo/lichess-cheat/master/showcase(2).gif)

# What it does
Highlight above the board the best next move for you.

# How it works?
The program will wait for the opponent turn depend on the clients chosen color.</br>
Then it will loop through every cell to detect the last moveset and feed the stockfish engine.</br>
Which will predict the best next move for the client.</br>
The clients moves are gathered by detecting the</br>
position where the client clicked on the board. And then translated to a moveset.</br>
In the old method we captured every 501 milliseconds the board to detect the last moveset.</br>
That brought up a big problem because if the opponent moved too fast we would miss</br>
the clients move. Using this method you can even play bullet mode. 

# Requirements
1) Pyautogui - in order to snap the images https://pypi.org/project/PyAutoGUI/
2) Open-cv - https://pypi.org/project/opencv-python/
3) Stockfish - https://pypi.org/project/stockfish/
4) Numpy - https://pypi.org/project/numpy/
5) Pynput - https://pypi.org/project/pynput/
6) Win32gui - https://pypi.org/project/win32gui/

# How to make it work
1) Download the main.py and the data folder
2) Download stockfish from here: https://stockfishchess.org/download/ I'v used "64-bit: Maximally compatible but slow."
3) You need to extract the exe file you downloaded and in main.py code, change the path to your stockfish engine exe file.
4) About the stockfish.set_depth(16) you can put higher values. The higher the value the more accurate the prediction
   But it's also slower. Using set depth 16 I tied against stockfish level 8 so it's preety strong as it is.
5) Open up liches site and open a game. Now open the program and choose your color.</br>
   Keep in mind that after you open the program. Dont click on your mouse anywhere</br>
   but the board.
   

# Compatibility Issues
~~The program is far from being perfect. It has a delay because it snap images.</br>
In order to detect pieces and it makes it vulnerable for crashing if the oppenent moved too fast.</br>
The cause is it takes time to detect client move (about half a second). </br>
If the opponent moved faster than that (By preselecting his move). </br>
Then the program will miss the clients move. And any predictions from this point will be wrong.</br>
This can be fixed by detecting last mouse click position. But as far</br>
as education challenge this project is done.</br>
Don't even bother trying Bullet mode. It can barley handle Blitz. In long time modes like Rapid or Classical it works perfectly.~~ (Fixed)
* The program only tested with Chrome on resolution 1920x1080 and the zoom needs to be 100%
* Technically you can make the program to work with any kind of browser on any kind of zoom.
  As long as you fix the cordinates of the board screenshot and the cell size.
* The program is more stable now but need to get a better check on mouse clicks.</br>
  In order to avoid missread client moves. 3 conditions needs to be checked to make it perfect:
  1) Check if board is visible.
  2) Check if mouse clicked within board rectangle.
  3) Check if move is legal as in between a1 - h8.

# Future plans
* ~~Adding support for black pieces~~ (Added).
* ~~Saving games played~~ (Added).
* ~~Auto Play~~ (Added check it out through the config. Only works for white player)
* Loading game movesets from File.
* ~~Drawing live on the board to highlight best next move.~~
* More stable clients moves read.

# Disclaimer 
**This entire project done for the purpose of challenge and education.**<br>
**Not for the purpose of cheating**

**Developed on Python 3.7.7**
