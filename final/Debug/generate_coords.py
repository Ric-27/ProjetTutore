#python configure.py -v ../ric_test.mp4
import cv2
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-img", "--image", type=str, help="path to the configuration image", default="../reference.jpg")
args = vars(ap.parse_args())

img = cv2.imread(args["image"],-1)

DESIRED_HEIGHT = 720
scale = DESIRED_HEIGHT/img.shape[0]
scaled_width = int(img.shape[1]*scale)
img = cv2.resize(img, (scaled_width,DESIRED_HEIGHT), interpolation = cv2.INTER_AREA)

points = []

global_coord_updated = False
global_x = 0
global_y = 0


def click(event, x, y, flags, param):
    global global_x,global_y,global_coord_updated
    if event == cv2.EVENT_LBUTTONDOWN:
        global_x = x
        global_y = y
        global_coord_updated = True

cv2.namedWindow("Configuration")
cv2.setMouseCallback("Configuration", click)

while True:
    if global_coord_updated:
        points.append([global_x,global_y])
        global_coord_updated = False

    points_np = np.array(points)
    for pt in points_np:
            cv2.circle(img,(pt[0],pt[1]),5,(255,100,100),-2)

    cv2.imshow("Configuration", img)

    key = cv2.waitKey(1)

    if key == ord('q'):
        print("file saved")
        print(points_np)
        np.savetxt('input_coordinates.txt',points_np, fmt='%d')
        break

cv2.destroyAllWindows()