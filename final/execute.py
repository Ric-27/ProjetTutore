import cv2
import numpy as np
import argparse
import random
from numpy.core.numeric import Infinity

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", type=str, help="path to the configuration file", default="data.npz")
ap.add_argument("-i", "--input", type=str, help="path to the input file", default="input_coordinates.txt")
ap.add_argument("-v", "--view", type=bool, help="view results in the reference image", default=False)
args = vars(ap.parse_args())


data = np.load(args["config"],allow_pickle=True)
points = np.loadtxt(args["input"],dtype=int)
output_points = [] 

DESIRED_HEIGHT = data['DESIRED_HEIGHT']
scale = data['scale']
pts_src = data['pts_src']
pts_dst = data['pts_dst']
#print(pts_dst)
pts_planes_h =  data['pts_planes']
#print(pts_planes_h)

h, status = cv2.findHomography(pts_src, pts_dst)

def transform_point(pt,h):
    pts_h = np.copy(pt[:2])
    pts_h = np.concatenate((pts_h,[1]),axis=0)
    pts_h = h@pts_h.transpose()
    pts_h = pts_h.transpose()
    pts_h[:] = pts_h[:]/pts_h[2]
    pts_h = pts_h[0:2]
    #pts_h = pts_h*scale
    pts_h = np.round(pts_h,0)
    return pts_h

for pt in points:
    pts_h = transform_point(pt,h)
    z = 0
    for plane in pts_planes_h:
        pts_plane_draw = np.array(plane[:,:2]).reshape((-1,1,2)).astype(np.int32)
        if cv2.pointPolygonTest(pts_plane_draw,(pts_h[0],pts_h[1]),measureDist = False) >= 0:
            if (plane[0,2] > z):
                z = plane[0,2]
                

    pts_h /= 100
    pts_h = pts_h.tolist()
    pts_h.append(z)
    pts_h = np.array(pts_h,dtype=np.float64)
    output_points.append(pts_h)

output_points = np.array(output_points,dtype=np.float64)
np.savetxt('output_coordinates.txt',output_points,fmt='%.2f')
print('coordinates transformed')
for i,pt in enumerate(points,0):
    print("pixel {} is at {}".format(pt,output_points[i]))

if args["view"] == True:
    img = cv2.imread("reference.jpg",-1)
    img_r = np.copy(img)
    run = True
    while run:
        for i,pt in enumerate(points,0):
            for j,pts in enumerate(pts_src,0):
                cv2.putText(img, "{},{}".format(pts_dst[j][0]/100,pts_dst[j][1]/100), (pts[0] + 5,pts[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200,200,200), 1)
                cv2.circle(img,(pts[0],pts[1]),4,(200,200,200),-1)
            b = random.randint(150,255)
            g = random.randint(150,255)
            r = random.randint(200,255)
            cv2.putText(img, "{}".format(output_points[i]), (pt[0] + 5,pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (b,g,r), 2)
            cv2.circle(img,(pt[0],pt[1]),4,(b,g,r),-2)
            cv2.imshow("result", img)
            key = cv2.waitKey(2000)
            img = np.copy(img_r)
            if key == ord('q'):
                run = False
                break
    cv2.destroyAllWindows()