import numpy as np
import cv2

cap = cv2.VideoCapture('ric_test_cut.mp4')

# take first frame of the video
ret, frame = cap.read()
# load the image, clone it, and setup the mouse callback function
reference = frame.copy()