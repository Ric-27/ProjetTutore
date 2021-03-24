import numpy as np
import cv2

cap = cv2.VideoCapture('ric_test.mp4')

# take first frame of the video
ret, frame = cap.read()
def Coords(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
            print("coords:", x, y)

cv2.imshow("Image", frame)
cv2.setMouseCallback("Image", Coords)

cv2.waitKey(0)
cv2.destroyAllWindows()
cap.release()