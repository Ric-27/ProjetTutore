import cv2
import numpy as np
import argparse
import random
from numpy.core.numeric import Infinity
from parameters import DESIRED_HEIGHT,MESUREMENT_SCALE

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", type=str, help="path to the configuration file", default="data.npz")
ap.add_argument("-i", "--input", type=str, help="path to the input file", default="input_coordinates.txt")
ap.add_argument("-img", "--image", type=str, help="path to the reference image", default="NONE")

ap.add_argument("-src", "--src", type=str, help="path to the source points", default="src.txt")
ap.add_argument("-dst", "--dst", type=str, help="path to the destination points", default="dst.txt")
ap.add_argument("-txt", "--txt", type=bool, help="use txt files", default=False)
args = vars(ap.parse_args())

read_txt = args["txt"]
if read_txt:
    pts_src = np.loadtxt("src.txt",dtype=int)
    pts_dst = np.loadtxt("dst.txt",dtype=int)
    h_z_planes =  []
    single_plane = False
else:
    data = np.load(args["config"],allow_pickle=True)
    pts_src = data['pts_src']
    pts_dst = data['pts_dst']
    h_z_planes =  data['z_planes']
    
    if h_z_planes.shape[0] == 1:
        single_plane = True
    else:
        single_plane = False

points = np.loadtxt(args["input"],dtype=int)
output_points = [] 

h, status = cv2.findHomography(pts_src, pts_dst)
h_inv, status = cv2.findHomography(pts_dst, pts_src)

if points.shape == (2,):
    single_point = True
else:
    single_point = False



z_planes = np.copy(h_z_planes)
for idx,plane in enumerate(h_z_planes,0):
    inv_z_plane = np.concatenate((plane[:,:2],np.ones([z_planes[idx].shape[0],1])),axis=1)
    inv_z_plane = h_inv@inv_z_plane.transpose()
    inv_z_plane = inv_z_plane.transpose()
    inv_z_plane[:,:] = inv_z_plane[:,:]/inv_z_plane[:,2:3]
    inv_z_plane = inv_z_plane[:,0:2]
    z_planes[idx] = np.concatenate((inv_z_plane.astype(np.int32),plane[:,2:3]),axis=1)

def transform_point(pt,h):
    pt_h = np.copy(pt[:2])
    pt_h = np.concatenate((pt_h,[1]),axis=0)
    pt_h = h@pt_h.transpose()
    pt_h = pt_h.transpose()
    pt_h[:] = pt_h[:]/pt_h[2]
    pt_h = pt_h[0:2]
    return pt_h

if single_point:
    h_points = transform_point(points,h)/MESUREMENT_SCALE
    h_points = np.round(h_points,2)
    output_points = np.concatenate((np.array(h_points,dtype=np.float64),[0]))
else:
    h_points = []
    for pt in points:
        pt_h = transform_point(pt,h)/MESUREMENT_SCALE
        pt_h = np.round(pt_h,2)
        h_points.append(pt_h)
    output_points = np.concatenate((np.array(h_points,dtype=np.float64),np.zeros([len(h_points),1])),axis=1)

if single_point:
    z = 0
    #for plane in z_planes:
    #    ref_z = plane[0,2]
    #    plane = np.array(plane[:,:2]).reshape((-1,1,2)).astype(np.int32)
    #    inside = cv2.pointPolygonTest(plane,(points[0],points[1]),measureDist = False)
    #    z = ref_z if z < ref_z and inside >= 0 else z               
    for plane in h_z_planes:
        ref_z = plane[0,2]
        plane = np.array(plane[:,:2]).reshape((-1,1,2)).astype(np.int32)
        inside = cv2.pointPolygonTest(plane,(int(output_points[0]*MESUREMENT_SCALE),int(output_points[1]*MESUREMENT_SCALE)),measureDist = False)
        z = ref_z if z < ref_z and inside >= 0 else z
    output_points[2] = z
else:
    for i,pt in enumerate(output_points,0):
        z = 0
        point = points[i]
        for plane in z_planes:
            ref_z = plane[0,2]
            plane = np.array(plane[:,:2]).reshape((-1,1,2)).astype(np.int32)
            inside = cv2.pointPolygonTest(plane,(point[0],point[1]),measureDist = False)
            z = ref_z if z < ref_z and inside >= 0 else z
        h_z = 0                
        for plane in h_z_planes:
            h_ref_z = plane[0,2]
            plane = np.array(plane[:,:2]).reshape((-1,1,2)).astype(np.int32)
            inside = cv2.pointPolygonTest(plane,(int(pt[0]*MESUREMENT_SCALE),int(pt[1]*MESUREMENT_SCALE)),measureDist = False)
            h_z = h_ref_z if h_z < h_ref_z and inside >= 0 else h_z
        
        if z != h_z:
            print("INCONGRUENCY: point {} has 2 different z values, transforming the plane with the inverse homography gave:({}), transforming the point with homography gave:({}). Assigning Homography value".format((pt[0],pt[1]),z,h_z))
        output_points[i,2] = h_z

output_points = np.array(output_points,dtype=np.float64)
np.savetxt('output_coordinates.txt',output_points,fmt='%.2f')
print('Coordinates Transformed and Saved to FILE')

if single_point:
    print("pixel {} is at {}".format(points,output_points))
else:
    for i,pt in enumerate(points,0):
        print("pixel {} is at {}".format(pt,output_points[i]))

if not args["image"] == "NONE":
    img = cv2.imread(args["image"],-1)

    scale = DESIRED_HEIGHT/img.shape[0]
    scaled_width = int(img.shape[1]*scale)
    img = cv2.resize(img, (scaled_width,DESIRED_HEIGHT), interpolation = cv2.INTER_AREA)
    
    window_width = max(pts_dst[:,0])
    window_height = max(pts_dst[:,1])
    h, status = cv2.findHomography(pts_src, pts_dst)
    h_img = cv2.warpPerspective(img, h, (window_width,window_height))

    h_scale = DESIRED_HEIGHT/h_img.shape[0]
    scaled_width = int(h_img.shape[1]*h_scale)
    h_img = cv2.resize(h_img, (scaled_width,DESIRED_HEIGHT), interpolation = cv2.INTER_AREA)

    run = True
    while run:
        for j,pts in enumerate(pts_src,0):
            #cv2.putText(img, "{},{}".format(pts_dst[j][0]/MESUREMENT_SCALE,pts_dst[j][1]/MESUREMENT_SCALE), (pts[0] + 5,pts[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
            cv2.circle(img,(pts[0],pts[1]),4,(0,0,255),-1)
            #cv2.circle(h_img,(int(pts_dst[j][0]*h_scale),int(pts_dst[j][1]*h_scale)),4,(0,0,255),-1)
        if single_plane:
            plane = z_planes[:,0:2].reshape((-1,1,2))
            cv2.polylines(img,np.int32([plane]),True,(200,0,255),2)
            plane = h_z_planes[:,0:2].reshape((-1,1,2))
            cv2.polylines(h_img,np.int32([plane]),True,(200,0,255),2)
        else:
            for i,plane in enumerate(z_planes,0):
                plane = plane[:,0:2].reshape((-1,1,2))
                cv2.polylines(img,np.int32([plane]),True,(200,0,255),2)
                plane = h_z_planes[i]
                plane = plane[:,0:2].reshape((-1,1,2))
                cv2.polylines(h_img,np.int32([plane]),True,(200,0,255),2)
        if single_point:
            cv2.putText(img, "{}".format(output_points), (points[0] + 5, points[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,255), 2)
            cv2.circle(img,(points[0] + 5, points[1]),4,(200,200,255),-2)
            cv2.putText(h_img, "{}".format(output_points), (int(output_points[0]*MESUREMENT_SCALE*h_scale) + 5,int(output_points[1]*MESUREMENT_SCALE*h_scale)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,255), 2)
            cv2.circle(h_img,(int(output_points[0]*MESUREMENT_SCALE*h_scale),int(output_points[1]*MESUREMENT_SCALE*h_scale)),4,(200,200,255),-2)
        else:
            for i,pt in enumerate(points,0):
                cv2.putText(img, "{}".format(output_points[i]), (pt[0] + 5,pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,255), 2)
                cv2.circle(img,(pt[0],pt[1]),4,(200,200,255),-2)
                cv2.putText(h_img, "{}".format(output_points[i]), (int(output_points[i][0]*MESUREMENT_SCALE*h_scale) + 5,int(output_points[i][1]*MESUREMENT_SCALE*h_scale)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,255), 2)
                cv2.circle(h_img,(int(output_points[i][0]*MESUREMENT_SCALE*h_scale),int(output_points[i][1]*MESUREMENT_SCALE*h_scale)),4,(200,200,255),-2)


        cv2.imshow("Reference", img)
        cv2.imshow("Transformed", h_img)
        key = cv2.waitKey(1)
        if key == ord('q') or key == 27:
            run = False
            break
    cv2.destroyAllWindows()