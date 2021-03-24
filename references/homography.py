import numpy as np
import cv2

vidcap = cv2.VideoCapture('ric_test.mp4')

success,image = vidcap.read()

h = image.shape[0]
w = image.shape[1]
print("Dimension de l'image :",h,"lignes x",w,"colonnes")
# let us plot the image
cv2.imshow('original',image[0:100,0:100])

#H_true = np.array([[ 1.37054309e+00 , 3.26472981e-01 ,-9.09781842e+01],
#                   [ 3.46896567e-03,  1.65383589e+00, -7.78613246e+01],
#                   [ 1.73448284e-04,  1.14069045e-03 , 1.00000000e+00]])
#print('this the homography we want to estimate',H_true)

#im2 = cv2.warpPerspective(image, H_true, (w,h))

#cv2.imshow('distorted',im2)
cv2.waitKey(0)
cv2.destroyAllWindows()