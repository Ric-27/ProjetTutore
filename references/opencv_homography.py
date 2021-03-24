#!/usr/bin/env python

import cv2
import numpy as np

if __name__ == '__main__' :

    vidcap = cv2.VideoCapture('ric_test.mp4')
    success,im_src = vidcap.read()


    # Read source image.
    #im_src = cv2.imread('book2.jpg')
    # Four corners of the book in source image
    pts_src = np.array([[378, 360], [915, 360],[1163, 630], [162, 630]], np.int32)


    # Read destination image.
    #im_dst = cv2.imread('book1.jpg')
    # Four corners of the book in destination image.
    pts_dst = np.array([[0, 0],[1185, 0],[1185, 820], [0, 820]], np.int32)

    # Calculate Homography
    h, status = cv2.findHomography(pts_src, pts_dst)
    
    # Warp source image to destination based on homography
    im_out = cv2.warpPerspective(im_src, h, (1185,820))
    
    # Display images
    pts = pts_src.reshape((-1,1,2))
    cv2.polylines(im_src,[pts],True,(0,255,255),10)
    cv2.imshow("Source Image", im_src)
    #cv2.imshow("Destination Image", im_dst)
    cv2.imshow("Warped Source Image", im_out)

    cv2.waitKey(0)
