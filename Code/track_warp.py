#code from https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

# import the necessary packages
import datetime
import imutils
import time
import cv2
import numpy as np
import math

cap = cv2.VideoCapture('ric_test.mp4')

pts_src = np.array([[475,211],[660,247],[1111,322],[915,360],[1163,630],[729,634],[370,638],[162,630],[67,428],[378,360],[233,308]], np.int32)
pts_dst = np.array([[200,0],[1170,1070],[2280,2170],[1680,2400],[1680,3220],[1110,3220],[730,3220],[500,3220],[30,2700],[500,2400],[0,2100]], np.int32)

minArea = 1300
threshold = 10

thickness = 2

window_width = 2280
window_height = 3220
scale = 0.2


# initialize the first frame in the video stream
reference = None

# loop over the frames of the video
while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    img = cap.read()
    img = img[1]
    #text = "Unoccupied"

    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if img is None:
        break
    
    h, status = cv2.findHomography(pts_src, pts_dst)

    # Warp source image to destination based on homography
    frame = cv2.warpPerspective(img, h, (window_width,window_height))

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, height = math.floor(window_height*scale)) #change for frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
	
    # if the first frame is None, initialize it
    if reference is None:
        reference = gray
        continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(reference, gray)
    thresh = cv2.threshold(frameDelta, threshold, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < minArea:
            continue
        
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), thickness)
        cv2.circle(frame, (math.floor(x + w/2), y + h), 3, (0, 255, 255), -thickness)
        #text = "Moving"
        cv2.putText(frame, "{},{}".format((x + w/2)/scale/100,(y + h)/scale/100), (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), thickness)

    # draw the text and timestamp on the frame
    for pt in pts_src:
        #print(pt[1])
        cv2.circle(img,(pt[0],pt[1]),3,(0,255,255),-thickness)
    cv2.circle(frame,(0,0),5,(255,0,255),-thickness)
    #pts = pts_src.reshape((-1,1,2))
    #cv2.polylines(img,[pts],True,(255,255,0),thickness)
    img = imutils.resize(img, height = math.floor(window_height*scale))
    #img_hor = np.concatenate((img,frame), axis=1)
    #cv2.imshow("Feed", img_hor)

    # show the frame and record if the user presses a key
    cv2.imshow("Original Feed", img)
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    #img_hor = np.concatenate((thresh,frameDelta), axis=1)
    #cv2.imshow("Tracking Parameters", img_hor)
    
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key is pressed, break from the loop
    if key == ord("q"):
        break
    if key == ord("p"):
        kill = False
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord("p"):
                break
            if key == ord("q"):
                kill = True
                break
        if kill == True:
            break
# cleanup the camera and close any open windows
cap.release()
cv2.destroyAllWindows()