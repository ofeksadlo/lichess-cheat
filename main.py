import cv2, win32gui, win32con
from pyautogui import screenshot
import numpy as np
from string import ascii_lowercase
from stockfish import Stockfish
from datetime import datetime


# First we import the stcokfish engine with a few adjusted parameters
# The 7 threads is because I have 8 threads and you leave 1 for the system.
stockfish = Stockfish('C:\stockfish_20090216_x64_bmi2.exe', parameters={"Threads" : 7, "Ponder" : True, "Minimum Thinking Time": 20, "Skill Level": 20, "Hash":16, "Contempt": 0, "Slow Mover": 84})
# If this parameter will get to high the accuracy will get better but it can cause
# the entire program to crash.
stockfish.set_depth(16)

# Creating the board window later on we will draw on it the board with best possible moves highlighted
cv2.namedWindow('Board')
# Prioritizing the board window over other windows
hwnd = win32gui.GetForegroundWindow()
# Positining the board window change the values if you don't see it show up.
win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,-16,150,0,0,0)

# This function checks if it's the client turn or the opponent turn
# True for client turn | False for opponent turn
def checkTurn(turnImg):
    clientTurns = None
    clientTurns_template = cv2.imread('data/turn.dat')
    opponentTurns_template = cv2.imread('data/noturn.dat')
    PC_clientTurns_template = cv2.imread('data/pc_turn.dat')
    PC_opponentTurns_template = cv2.imread('data/pc_noturn.dat')
    if matchImages(turnImg, clientTurns_template) < 30 or matchImages(turnImg, PC_clientTurns_template) < 30:
        clientTurns = True
    elif matchImages(turnImg, opponentTurns_template) < 30 or matchImages(turnImg, PC_opponentTurns_template) < 30:
        clientTurns = False
    return clientTurns

# Check 2 images for missmatched pixels. The lower the number the better the match.
# (This is a very simple method for image matching but efficent for our cause.)
def matchImages(img1, img2):
    err = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
    err /= float(img1.shape[0]*img2.shape[1])
    return err

# Using this function we highlight the best moves possible
# The function gets the board and the moveset we want to highlight
# And returns the board with the highlighted cells
def drawOnBoard(board, moveset,whitePlayer, cellSize=92):

    letters = list(ascii_lowercase[:8])

    movedFromCell_whiteTemplate = cv2.imread('data/white_from.dat')
    movedFromCell_blackTemplate = cv2.imread('data/black_from.dat')
    movedToCell_whiteTemplate = cv2.imread('data/black_to.dat')
    movedToCell_blackTemplate = cv2.imread('data/white_to.dat')

    painted_board = board.copy()
    cell1 = moveset[0] + moveset[1]
    cell2 = moveset[2] + moveset[3]
    for y in range(8):
        for x in range(8):
            board_cell = board[x * cellSize:(x+1) * cellSize, y * cellSize:(y+1) * cellSize]
            if whitePlayer == True:
                if letters[y]+str(8-x) == cell1:
                    painted_board = cv2.rectangle(painted_board, (y*cellSize, x*cellSize), ((y+1)*cellSize, (x+1)*cellSize), (255,0,0), thickness=2)
                elif  letters[y]+str(8-x) == cell2:
                    painted_board = cv2.rectangle(painted_board, (y*cellSize, x*cellSize), ((y+1)*cellSize, (x+1)*cellSize), (255,0,0), thickness=2)
            elif whitePlayer == False:
                reversed_letters = letters[::-1]
                if reversed_letters[y]+str(x+1) == cell1:
                    painted_board = cv2.rectangle(painted_board, (y*cellSize, x*cellSize), ((y+1)*cellSize, (x+1)*cellSize), (255,0,0), thickness=2)
                elif  reversed_letters[y]+str(x+1) == cell2:
                    painted_board = cv2.rectangle(painted_board, (y*cellSize, x*cellSize), ((y+1)*cellSize, (x+1)*cellSize), (255,0,0), thickness=2)

    return painted_board



# Gets board image and return last moveset.
def getLastMove(board, whitePlayer, cellSize=92):
    e8LightGreen = False
    h8DarkGreen = False
    a8LightGreen = False
    h1LightGreen = False
    a1DarkGreen = False
    e1DarkGreen = False
    castling = False
    # Reading the cell templates later on we will match them to the board cells.
    movedFromCell_whiteTemplate = cv2.imread('data/white_from.dat')
    movedFromCell_blackTemplate = cv2.imread('data/black_from.dat')
    movedToCell_whiteTemplate = cv2.imread('data/black_to.dat')
    movedToCell_blackTemplate = cv2.imread('data/white_to.dat')
    # Creating a list with alphabet range a-h (8 letters total).
    letters = list(ascii_lowercase[:8])
    lastMoveSet = ['','']
    # We are looping from the top left corner of the board
    for y in range(8):
        for x in range(8):
            # Initializing the board cell according to the cell size
            board_cell = board[x * cellSize:(x+1) * cellSize, y * cellSize:(y+1) * cellSize]
            # Here we check the board cell to match with are templates.
            # We first check if the cell is where the piece moved from.
            # Because it's supposed to be an absolute match (same exact picture).
            # We check first for the white template then for the black template.
            # The reason is that if a piece moved from a black color
            # it will have a diffrent color, if it moved from a white piece.
            # If the cell is not piece that moved from. Then
            # we check if it's a piece that moved to this cell. Again for both templates white and black.
            

            # In this "long" if statements all we check for is matching colors.
            # If the cell in the top left corner is green. And in the middle is green as well. Then
            # we found where the player moved from. Otherwise if the cell is green at the top left
            # but not green in the middle. Then it has to be where the player moved to.

            # Further more we check for possible castling that is why we check for cells e8, a8, h8.
            # Because this are the possible castling cells of the opponent and are method won't work.
            # Because we will have in this moveset(for example e8g8) 2 empty green cells.
            if whitePlayer == True:
                if matchImages(board_cell[1:2, 1:2], movedFromCell_whiteTemplate[1:2,1:2]) < 10 and matchImages(board_cell[45:47,45:47], movedFromCell_whiteTemplate[45:47,45:47])<10:
                    if letters[y]+str(8-x) == 'e8':
                        e8LightGreen = True
                    elif letters[y]+str(8-x) == 'a8':
                        a8LightGreen = True
                    lastMoveSet[0] = letters[y]+str(8-x)
                elif matchImages(board_cell[1:2, 1:2], movedFromCell_blackTemplate[1:2,1:2]) < 10 and matchImages(board_cell[45:47,45:47], movedFromCell_blackTemplate[45:47,45:47])<10:
                    if letters[y]+str(8-x) == 'h8':
                        h8DarkGreen = True
                    lastMoveSet[0] = letters[y]+str(8-x)
                elif matchImages(board_cell[1:2, 1:2], movedToCell_whiteTemplate[1:2,1:2]) < 10:
                    lastMoveSet[1] = letters[y]+str(8-x)
                elif matchImages(board_cell[1:2, 1:2], movedToCell_blackTemplate[1:2,1:2]) < 10:
                    lastMoveSet[1] = letters[y]+str(8-x)
            elif whitePlayer == False:
                reversed_letters = letters[::-1]
                if matchImages(board_cell[1:2, 1:2], movedFromCell_whiteTemplate[1:2,1:2]) < 10 and matchImages(board_cell[45:47,45:47], movedFromCell_whiteTemplate[45:47,45:47])<10:
                    if reversed_letters[y]+str(x+1) == 'e8':
                        e8LightGreen = True
                    elif reversed_letters[y]+str(x+1) == 'a8':
                        a8LightGreen = True
                    elif reversed_letters[y]+str(x+1) == 'h1':
                        h1LightGreen = True
                    lastMoveSet[0] = reversed_letters[y]+str(x+1)
                elif matchImages(board_cell[1:2, 1:2], movedFromCell_blackTemplate[1:2,1:2]) < 10 and matchImages(board_cell[45:47,45:47], movedFromCell_blackTemplate[45:47,45:47])<10:
                    if reversed_letters[y]+str(x+1) == 'e1':
                        e1DarkGreen = True
                    elif reversed_letters[y]+str(x+1) == 'a1':
                        a1DarkGreen = True
                    elif letters[y]+str(8-x) == 'h8':
                        h8DarkGreen = True
                    lastMoveSet[0] = reversed_letters[y]+str(x+1)
                elif matchImages(board_cell[1:2, 1:2], movedToCell_whiteTemplate[1:2,1:2]) < 10:
                    lastMoveSet[1] = reversed_letters[y]+str(x+1)
                elif matchImages(board_cell[1:2, 1:2], movedToCell_blackTemplate[1:2,1:2]) < 10:
                    lastMoveSet[1] = reversed_letters[y]+str(x+1)
    # We check if it is a castling
    if e8LightGreen == True and h8DarkGreen == True and castling == False:
        castling = True
        return ["e8", "g8"]
    elif e8LightGreen == True and a8LightGreen == True and castling == False:
        castling = True
        return ["e8", "c8"]
    elif e1DarkGreen == True and h1LightGreen == True:
        castling = True
        return ["e1", "g1"]
    elif e1DarkGreen == True and a1DarkGreen == True:
        return ["e1", "c1"]
    # If nothing moved we return ''
    if lastMoveSet[0] == '' or lastMoveSet[1] == '':
        return ''

    return lastMoveSet


# Now we have all the methods we need. We start by creating all the necessary variables.

# Into board we will screenshot the frame. And the detect last moveset
board = None 
# When starting a game each player gets a long time for the first turn.
# For blitz it's 30 seconds and during this time there is no indication who's turn is it. This
# is why we use firstTurn variable
firstTurn = True
# As we start off as white the first to play is the white.
clientTurns = True
# This variable will contain the entire movesets of the game. We append
# each moveset at a time and then get the next best move from stockfish engine.
gameMoveSet = []
# Here we store the last moveset.
lastMove = ["",""]
# Storing the next best move to later on send it drawOnBoard.
nextBestMove = None
# Creating a log file of the last game.
f= open('logs/logFile.txt', 'a')
# Deleting the previous game moves.
f.write('')

playerColor = input('Insert your pieces color (\'b\' = black / \'w\' = white): ')
if playerColor == 'b':
    clientTurns = False
while True:
    # We snap which turn is it.
    screenshot('turn.png', region=(1335, 665,10,16))
    # If you wonder why we save the image and then reading it again is because cv2.imread() is diffrent than
    # the pyautogui.screenshot() object.
    turnImg = cv2.imread('turn.png')
    # We check if the turn changed
    newClientsTurn = checkTurn(turnImg)
    if clientTurns != newClientsTurn or firstTurn ==True:
        clientTurns = newClientsTurn
        if firstTurn == True:
            clientTurns = False
            firstTurn = False
        cv2.waitKey(250)
        screenshot('board.png', region=(575,164,735,735))
        board = cv2.imread('board.png')
        if getLastMove(board, (playerColor == 'w')) != '':
            nextLastMove = getLastMove(board, (playerColor == 'w'))
            if (lastMove[0] + lastMove[1]) != (nextLastMove[0] + nextLastMove[1]):
                lastMove = getLastMove(board, (playerColor == 'w'))
                gameMoveSet.append(lastMove[0] + lastMove[1])
                stockfish.set_position(gameMoveSet)
                print('Last moveset: ' + lastMove[0] + lastMove[1])
                f.write(lastMove[0] + lastMove[1]+'\n')
                nextBestMove = stockfish.get_best_move()
                print('Best next move: ' + nextBestMove)
                print("------------------")
    
    if nextBestMove is not None:
        board_show = cv2.imread('board.png')
        board_show = drawOnBoard(board_show, nextBestMove, (playerColor == 'w'))
        board_show = cv2.resize(board_show, None, fx=0.785, fy=0.785)
        cv2.imshow('Board', board_show)


    
    cv2.waitKey(1)
f.close()
