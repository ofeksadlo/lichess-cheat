import cv2, win32gui, win32con
from pyautogui import screenshot
import numpy as np
from string import ascii_lowercase
from stockfish import Stockfish
from datetime import datetime

stockfish = Stockfish('C:\stockfish_20090216_x64_bmi2.exe', parameters={"Threads" : 7, "Ponder" : True, "Skill Level": 20, "Contempt": 0, "Slow Mover": 84})

cv2.namedWindow('Board')
hwnd = win32gui.GetForegroundWindow()
win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,575,164,200,200,0)


def checkTurn(turnImg):
    clientTurns = None
    clientTurns_template = cv2.imread('data/turn.png')
    opponentTurns_template = cv2.imread('data/noturn.png')
    PC_clientTurns_template = cv2.imread('data/pc_turn.png')
    PC_opponentTurns_template = cv2.imread('data/pc_noturn.png')
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


def drawOnBoard(board, moveset, cellSize=92):

    letters = list(ascii_lowercase[:8])

    movedFromCell_whiteTemplate = cv2.imread('data/white_from.jpg')
    movedFromCell_blackTemplate = cv2.imread('data/black_from.jpg')
    movedToCell_whiteTemplate = cv2.imread('data/black_to.jpg')
    movedToCell_blackTemplate = cv2.imread('data/white_to.jpg')

    painted_board = board.copy()
    cell1 = moveset[0] + moveset[1]
    cell2 = moveset[2] + moveset[3]
    for y in range(8):
        for x in range(8):
            board_cell = board[x * cellSize:(x+1) * cellSize, y * cellSize:(y+1) * cellSize]
            if letters[y]+str(8-x) == cell1:
                painted_board = cv2.rectangle(painted_board, (y*cellSize, x*cellSize), ((y+1)*cellSize, (x+1)*cellSize), (255,0,0), thickness=2)
            elif  letters[y]+str(8-x) == cell2:
                painted_board = cv2.rectangle(painted_board, (y*cellSize, x*cellSize), ((y+1)*cellSize, (x+1)*cellSize), (255,0,0), thickness=2)

    return painted_board



# Gets board image and return last moveset.
def getLastMove(board, cellSize=92):
    e8LightGreen = False
    h8DarkGreen = False
    a8LightGreen = False
    castling = False
    # Reading the cell templates later on we will match them to the board cells.
    movedFromCell_whiteTemplate = cv2.imread('data/white_from.jpg')
    movedFromCell_blackTemplate = cv2.imread('data/black_from.jpg')
    movedToCell_whiteTemplate = cv2.imread('data/black_to.jpg')
    movedToCell_blackTemplate = cv2.imread('data/white_to.jpg')
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
            #
            #There is an image example in Examples folder

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
            
    if e8LightGreen == True and h8DarkGreen == True and castling == False:
        castling = True
        return ["e8", "g8"]
    elif e8LightGreen == True and a8LightGreen == True and castling == False:
        castling = True
        return ["e8", "c8"]

    if lastMoveSet[0] == '' or lastMoveSet[1] == '':
        return ''

    return lastMoveSet

board = None
firstTurn = 2
clientTurns = True
gameMoveSet = []
lastMove = ["",""]
nextBestMove = None
f= open('logs/logFile.txt', 'a')
f.write('')
while True:
    # win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    screenshot('turn.png', region=(1335, 665,10,16))
    turnImg = cv2.imread('turn.png')
    newClientsTurn = checkTurn(turnImg)
    if clientTurns != newClientsTurn or firstTurn > 0:
        clientTurns = newClientsTurn
        if firstTurn > 0:
            cv2.waitKey(1500)
        cv2.waitKey(500)
        screenshot('board.png', region=(575,164,735,735))
        board = cv2.imread('board.png')
        if getLastMove(board) != '':
            nextLastMove = getLastMove(board)
            if (lastMove[0] + lastMove[1]) != (nextLastMove[0] + nextLastMove[1]):
                if firstTurn > 0:
                    firstTurn -= 1
                lastMove = getLastMove(board)
                gameMoveSet.append(lastMove[0] + lastMove[1])
                stockfish.set_position(gameMoveSet)
                print('Last moveset: ' + lastMove[0] + lastMove[1])
                f.write(lastMove[0] + lastMove[1]+'\n')
                nextBestMove = stockfish.get_best_move()
                print('Best next move: ' + nextBestMove)
                print("------------------")
    
    if nextBestMove is not None:
        board_show = cv2.imread('board.png')
        board_show = drawOnBoard(board_show, nextBestMove)
        board_show = cv2.resize(board_show, None, fx=0.5, fy=0.5)
        # print(nextBestMove)
        # win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,575,164,735,735,0)
        cv2.imshow('Board', board_show)


    
    cv2.waitKey(1)
f.close()
