import cv2
from pyautogui import screenshot
import numpy as np
from string import ascii_lowercase
import win32gui
import win32con

hwnd = win32gui.GetForegroundWindow()
win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,100,100,200,200,0)

# import os
# os.system("mode con cols=50 lines=20")

clientTurns = True
# Check 2 images for missmatched pixels. The lower the number the better the match.
# (This is a very simple method for image matching but efficent for our cause.)
def matchImages(img1, img2):
    err = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
    err /= float(img1.shape[0]*img2.shape[1])
    return err

# Using image matching we will check if it's the client turnImg.
# Further more we will test if the client is on game to avoid failing.
def checkTurn(turnImg):
    clientTurns = None
    clientTurns_template = cv2.imread('data/turn.png')
    opponentTurns_template = cv2.imread('data/noturn.png')
    if matchImages(turnImg, clientTurns_template) < 30:
        clientTurns = True
    elif matchImages(turnImg, opponentTurns_template) < 30:
        clientTurns = False
    return clientTurns

# Gets board image and return last moveset.
def getLastMove(board, cellSize=92):
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
            if matchImages(board_cell[1:2, 1:2], movedFromCell_whiteTemplate[1:2,1:2]) < 10 and matchImages(board_cell[45:47,45:47], movedFromCell_whiteTemplate[45:47,45:47])<10:
                    lastMoveSet[0] = letters[y]+str(8-x)
            elif matchImages(board_cell[1:2, 1:2], movedFromCell_blackTemplate[1:2,1:2]) < 10 and matchImages(board_cell[45:47,45:47], movedFromCell_blackTemplate[45:47,45:47])<10:
                    lastMoveSet[0] = letters[y]+str(8-x)
            elif matchImages(board_cell[1:2, 1:2], movedToCell_whiteTemplate[1:2,1:2]) < 10:
                    lastMoveSet[1] = letters[y]+str(8-x)
            elif matchImages(board_cell[1:2, 1:2], movedToCell_blackTemplate[1:2,1:2]) < 10:
                    lastMoveSet[1] = letters[y]+str(8-x)
            
    if lastMoveSet[0] == '' or lastMoveSet[1] == '':
        return ''
    return lastMoveSet

lastMove = ['','']
while True:
    # screenshot('turn.png', region=(1326, 670,78,16))
    # turnImg = cv2.imread('turn.png')
    screenshot('board.png', region=(575,164,735,735))
    board = cv2.imread('board.png')
    if getLastMove(board) != '':
        if lastMove != getLastMove(board):
            lastMove = getLastMove(board)
            print(lastMove)
            # cv2.waitKey(1000)
    
    cv2.waitKey(1000)


    
    
# board = cv2.imread('frame.png')

# print(getLastMove(board))
