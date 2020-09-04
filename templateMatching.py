import cv2, time
import numpy as np
from  pyautogui import screenshot

time.sleep(3)
frame = screenshot('frame.png', region=(575,164,735,735))