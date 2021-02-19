import numpy as np
import cv2
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys


def generate_markers():
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

    fig = plt.figure()
    nx = 4
    ny = 4
    for i in range(1, nx*ny+1):
        ax = fig.add_subplot(ny,nx, i)
        img = aruco.drawMarker(aruco_dict,i, 700)
        plt.imshow(img, cmap = mpl.cm.gray, interpolation = "nearest")
        ax.axis("off")
    plt.savefig("marker/markers.pdf")
    plt.show()

def detect_markers(image):
    frame = cv2.imread(image)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

    plt.figure()
    plt.imshow(frame_markers)
    for i in range(len(ids)):
        c = corners[i][0]
        plt.plot([c[:, 0].mean()], [c[:, 1].mean()], "o", label = "id={0}".format(ids[i]))
        #plt.plot([c[:, 0]], [c[:, 1]], ".")
    plt.legend()
    '''
    for i in range(len(ids)):
        c = corners[i][0]
        plt.plot([c[:, 0]], [c[:, 1]], ".")
    '''
    plt.show()

if __name__=="__main__":
    
    if len(sys.argv) != 2:
        image = "../marker/bedroomMoreMarkerDataset/1_1.jpg"
    else:
        image = sys.argv[1]
    detect_markers(image)