import cv2
from pyautogui import screenshot
import numpy as np
from string import ascii_lowercase

# Check 2 images for missmatched pixels. The lower the number the better the match
def matchImages(img1, img2):
    err = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
    err /= float(img1.shape[0]*img2.shape[1])
    return err
# Gets board image and return last moveset.
def getLastMove(board, cellSize=92):
    # Reading the cell templates later on we will match them to the board cells.
    movedFromCell_whiteTemplate = cv2.imread('data/white_from.jpg')
    movedToCell_whiteTemplate = cv2.imread('data/white_to.jpg')
    movedFromCell_blackTemplate = cv2.imread('data/black_from.jpg')
    movedToCell_blackTemplate = cv2.imread('data/black_to.jpg')
    # Creating a list with alphabet range a-h (8 letters total).
    letters = list(ascii_lowercase[:8])
    lastMoveSet = ''
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
            if matchImages(board_cell[1:2, 1:2], movedFromCell_whiteTemplate[1:2,1:2]) < 10 and matchImages(board_cell[45:47,45:47], movedFromCell_whiteTemplate[45:47,45:47])<10:
                lastMoveSet += letters[y]+str(8-x)
            elif matchImages(board_cell[1:2, 1:2], movedFromCell_blackTemplate[1:2,1:2]) < 10 and matchImages(board_cell[45:47,45:47], movedFromCell_blackTemplate[45:47,45:47])<10:
                lastMoveSet += letters[y]+str(8-x)
            elif matchImages(board_cell[1:2, 1:2], movedFromCell_whiteTemplate[1:2,1:2]) < 10:
                lastMoveSet += letters[y]+str(8-x)
            elif matchImages(board_cell[1:2, 1:2], movedFromCell_blackTemplate[1:2,1:2]) < 10:
                lastMoveSet += letters[y]+str(8-x)
    return lastMoveSet

board = cv2.imread('frame.png')
print(getLastMove(board))

cv2.imshow('', board)
cv2.waitKey(0)
