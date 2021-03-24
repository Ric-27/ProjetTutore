#code from https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
# and https://www.geeksforgeeks.org/reading-writing-text-files-python/

# import the necessary packages
import datetime
import imutils
import time
import cv2
import numpy as np
import math

cap = cv2.VideoCapture('ric_test.mp4')
success,img = cap.read()

#pts_src = np.array([[475,211,0],[660,247,0],[1111,322,0],[915,360,0],[1163,630,0],[729,634,0],[370,638,0],[162,630,0],[67,428,0],[378,360,0],[233,308,0]], np.int32)
pts_dst = np.array([[200,0,0],[1170,1070,0],[2280,2170,0],[1680,2400,0],[1680,3220,0],[1110,3220,0],[730,3220,0],[500,3220,0],[30,2700,0],[500,2400,0],[0,2100,0]], np.int32)

#np.savetxt("config.txt",pts_src)

pts_src = np.loadtxt("config.txt",dtype=np.int32)

pts_plane1 = np.array([[480,397,1],[816,395,1],[819,404,1],[479,406,1]],np.int32)
pts_plane2 = np.array([[482,374,2],[815,372,2],[819,375,2],[480,377,2]],np.int32)

pts_planes = np.array([pts_src,pts_plane1,pts_plane2],dtype=object)

pts_interest = np.array([[655,513,0],[812,400,1],[484,375,2]],np.int32)

h, status = cv2.findHomography(pts_src, pts_dst)

minArea = 1000
threshold = 16

lineThickness = 2

seconds = 0.1
fps = cap.get(cv2.CAP_PROP_FPS) # Gets the frames per second
multiplier = fps * seconds

window_width = max(pts_dst[:,0])
window_height = max(pts_dst[:,1])
scale = 0.23

# initialize the first frame in the video stream
reference = None

#
pts_planes_frame = np.copy(pts_planes)
for idx,plane in enumerate(pts_planes,0):
    pts_plane_frame = np.copy(plane[:,:2])
    pts_plane_frame = np.concatenate((plane[:,:2],np.ones([pts_planes_frame[idx].shape[0],1])),axis=1)
    pts_plane_frame = h@pts_plane_frame.transpose()
    pts_plane_frame = pts_plane_frame.transpose()
    pts_plane_frame[:,:] = pts_plane_frame[:,:]/pts_plane_frame[:,2:3]
    pts_plane_frame = pts_plane_frame[:,0:2]
    pts_plane_frame = pts_plane_frame*scale
    pts_plane_frame = np.round(pts_plane_frame,0)
    pts_planes_frame[idx] = np.concatenate((pts_plane_frame.astype(np.int32),plane[:,2:3]),axis=1)

pts_interest_frame = np.copy(pts_interest)
for idx,pt in enumerate(pts_interest,0):
    pts_frame = np.copy(pt[:2])
    pts_frame = np.concatenate((pts_frame,[1]),axis=0)
    pts_frame = h@pts_frame.transpose()
    pts_frame = pts_frame.transpose()
    pts_frame[:] = pts_frame[:]/pts_frame[2]
    pts_frame = pts_frame[0:2]
    pts_frame = pts_frame*scale
    pts_frame = np.round(pts_frame,0)
    pts_interest_frame[idx] = np.concatenate((pts_frame.astype(np.int32),[pt[2]]),axis=0)

# loop over the frames of the video
while success:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    frameId = int(round(cap.get(1)))
    success, img = cap.read()
    #img = img[1]

    if frameId % multiplier == 0:
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

        for idx,plane in enumerate(pts_planes,0):
            if idx != 0:
                pts_plane = plane[:,0:2].reshape((-1,1,2))
                cv2.polylines(img,np.int32([pts_plane]),True,(255,0,0,50),lineThickness)

        for idx,plane in enumerate(pts_planes_frame,0):
            if idx != 0:
                pts_plane_frame = plane[:,0:2].reshape((-1,1,2))
                cv2.polylines(frame,np.int32([pts_plane_frame]),True,(255,0,0,50),lineThickness)

        for pt in pts_interest:
                cv2.circle(img,(pt[0],pt[1]),5,(0,255,255,50),lineThickness)

        for pt in pts_interest_frame:
                cv2.circle(frame,(pt[0],pt[1]),5,(0,255,255,50),lineThickness)

        for pt in pts_src:
            cv2.circle(img,(pt[0],pt[1]),5,(255,0,255),lineThickness)
        
        cv2.circle(frame,(0,0),10,(0,0,255),-lineThickness)

        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < minArea:
                continue
            
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), lineThickness)
            cv2.circle(frame, (round(x + w/2), y + h - 10), 3, (255, 255, 255), -lineThickness)

            x_cm = (x + w/2)/scale
            y_cm = (y + h - 10)/scale
            z = -1
            for plane in pts_planes_frame:
                if x_cm*scale > min(plane[:,0]) and x_cm*scale < max(plane[:,0]) and y_cm*scale < max(plane[:,1]) and y_cm*scale > min(plane[:,1]):
                    if (plane[0,2] > z):
                        z = plane[0,2]

            for pt in pts_interest_frame:
                if pt[2] == z:
                    cv2.line(frame,(round(x_cm*scale),round(y_cm*scale)),(pt[0],pt[1]),(0,255,255),lineThickness)

            cv2.putText(frame, "x: {}".format(round(x_cm/100,2)), (x, y + h - 42), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, "y: {}".format(round(y_cm/100,2)), (x, y + h - 28), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, "z: {}".format(z), (x, y + h - 14), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        #pts_plane2_frame = pts_plane2.reshape((-1,1,2))
        #cv2.polylines(img,[pts_plane2_frame],True,(255,0,0),lineThickness)

        # show the frame and record if the user presses a key
        #cv2.imshow("Original Feed", img)
        #cv2.imshow("Security Feed", frame)
        #cv2.imshow("Thresh", thresh)
        #cv2.imshow("Frame Delta", frameDelta)

        img = imutils.resize(img, height = frame.shape[0])
        img_hor = np.concatenate((img,frame), axis=1)
        cv2.imshow("Feed", img_hor)
        
        #img_hor = np.concatenate((thresh,frameDelta), axis=1)
        #cv2.imshow("Tracking Parameters", img_hor)
        
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the loop
        if key == ord("q"):
            break
        if key == ord("p"):
            kill = False
            while True:
                key = cv2.waitKey(200) & 0xFF
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