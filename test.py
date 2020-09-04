import cv2
from pyautogui import screenshot
import numpy as np
import time
from string import ascii_lowercase


def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

# time.sleep(3)
# frame = screenshot('frame.png', region=(575,164,735,735))
# #

letters = list(ascii_lowercase[:7])


frame = cv2.imread('frame.png')

fromTemplate_white = cv2.imread('data/white_from.jpg')
toTemplate_white = cv2.imread('data/white_to.jpg')
fromTemplate_black = cv2.imread('data/black_from.jpg')
toTemplate_black = cv2.imread('data/black_to.jpg')
cell = cv2.imread('props/a4.jpg')
for i in range(8):
    for j in range(8):        
        # frame = cv2.rectangle(frame, (i*92,j*92), (((i+1)*92), (j+1)*92), (0, 0, 255), thickness=2)
        # print((i*92,j*92), (((i+1)*92), (j+1)*92))
        prop = frame[j*92:(j+1)*92,i*92:((i+1)*92)]

        # 
        if mse(prop[1:2,1:2], fromTemplate_white[1:2,1:2]) < 10 and mse(prop[45:47, 45:47], fromTemplate_white[45:47,45:47]) < 10:
            print('Move from cell: ' + letters[i]+str(8-j)+'.jpg')
        elif mse(prop[1:2,1:2], fromTemplate_black[1:2,1:2]) < 10 and mse(prop[45:47, 45:47], fromTemplate_black[45:47,45:47]) < 10:
            print('Move from cell: ' + letters[i]+str(8-j)+'.jpg')
        elif mse(prop[1:2,1:2], fromTemplate_white[1:2,1:2]) < 10:
            print('Move to cell: ' + letters[i]+str(8-j)+'.jpg')
        elif mse(prop[1:2,1:2], fromTemplate_black[1:2,1:2]) < 10:
            print('Move to cell: ' + letters[i]+str(8-j)+'.jpg')
        
        # cv2.imwrite('props/' + letters[i]+str(8-j)+'.jpg', prop)


cv2.imshow('frame', frame)
cv2.waitKey(0)
