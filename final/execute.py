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
if points.shape == (2,):
    single_point = True
else:
    single_point = False
output_points = [] 

DESIRED_HEIGHT = data['DESIRED_HEIGHT']
scale = data['scale']
pts_src = data['pts_src']
pts_dst = data['pts_dst']
#print(pts_dst)
z_planes =  data['z_planes']
#print(z_planes)
if z_planes.shape == (2,):
    single_plane = True
else:
    single_plane = False

single_plane = False

h, status = cv2.findHomography(pts_src, pts_dst)
h_inv, status = cv2.findHomography(pts_dst, pts_src)

inv_z_planes = np.copy(z_planes)
for idx,plane in enumerate(z_planes,0):
    inv_z_plane = np.concatenate((plane[:,:2],np.ones([inv_z_planes[idx].shape[0],1])),axis=1)
    inv_z_plane = h_inv@inv_z_plane.transpose()
    inv_z_plane = inv_z_plane.transpose()
    inv_z_plane[:,:] = inv_z_plane[:,:]/inv_z_plane[:,2:3]
    inv_z_plane = inv_z_plane[:,0:2]
    #inv_z_plane = inv_z_plane*scale
    inv_z_planes[idx] = np.concatenate((inv_z_plane.astype(np.int32),plane[:,2:3]),axis=1)

def transform_point(pt,h):
    pt_h = np.copy(pt[:2])
    pt_h = np.concatenate((pt_h,[1]),axis=0)
    pt_h = h@pt_h.transpose()
    pt_h = pt_h.transpose()
    pt_h[:] = pt_h[:]/pt_h[2]
    pt_h = pt_h[0:2]
    #pt_h = pt_h*scale
    #pt_h = np.round(pt_h,0)
    return pt_h

if single_point:
    z = 0
    for plane in inv_z_planes:
        ref_z = plane[0,2]
        plane = np.array(plane[:,:2]).reshape((-1,1,2)).astype(np.int32)
        inside = cv2.pointPolygonTest(plane,(points[0],points[1]),measureDist = False)
        if inside >= 0:
            if (ref_z > z):
                z = ref_z
    
    pt_h = transform_point(points,h)
    pt_h /= 100
    pt_h = np.concatenate((pt_h,[z]),axis=0)
    pt_h = np.round(pt_h,2)
    output_points.append(pt_h)
else:
    for pt in points:
        z = 0
        for plane in inv_z_planes:
            ref_z = plane[0,2]
            plane = np.array(plane[:,:2]).reshape((-1,1,2)).astype(np.int32)
            inside = cv2.pointPolygonTest(plane,(pt[0],pt[1]),measureDist = False)
            if inside >= 0:
                if (ref_z > z):
                    z = ref_z
        
        pt_h = transform_point(pt,h)
        pt_h /= 100
        pt_h = np.concatenate((pt_h,[z]),axis=0)
        pt_h = np.round(pt_h,2)
        output_points.append(pt_h)

output_points = np.array(output_points,dtype=np.float64)
np.savetxt('output_coordinates.txt',output_points,fmt='%.2f')
print('coordinates transformed')

if single_point:
    print("pixel {} is at {}".format(points,output_points))
else:
    for i,pt in enumerate(points,0):
        print("pixel {} is at {}".format(pt,output_points[i]))

if args["view"] == True:
    img = cv2.imread("reference.jpg",-1)
    img_r = np.copy(img)
    run = True
    while run:
        if single_point:
            for j,pts in enumerate(pts_src,0):
                cv2.putText(img, "{},{}".format(pts_dst[j][0]/100,pts_dst[j][1]/100), (pts[0] + 5,pts[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200,200,200), 1)
                cv2.circle(img,(pts[0],pts[1]),4,(200,200,200),-1)
            b = random.randint(150,255)
            g = random.randint(150,255)
            r = random.randint(200,255)
            if single_plane:
                for plane in inv_z_planes:
                    plane = plane[:,:,:2]
                    plane = plane.reshape((-1,1,2))
                    cv2.polylines(img,np.int32([plane]),True,(255,0,255),2)
            else:
                for plane in inv_z_planes:
                    plane = plane[:,0:2].reshape((-1,1,2))
                    cv2.polylines(img,np.int32([plane]),True,(255,0,255),2)

            cv2.putText(img, "{}".format(output_points), (points[0] + 5,points[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (b,g,r), 2)
            cv2.circle(img,(points[0],points[1]),4,(b,g,r),-2)
            cv2.imshow("result", img)
            key = cv2.waitKey(1000)
            img = np.copy(img_r)
            if key == ord('q'):
                run = False
                break
        else:
            for i,pt in enumerate(points,0):
                for j,pts in enumerate(pts_src,0):
                    cv2.putText(img, "{},{}".format(pts_dst[j][0]/100,pts_dst[j][1]/100), (pts[0] + 5,pts[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200,200,200), 1)
                    cv2.circle(img,(pts[0],pts[1]),4,(200,200,200),-1)
                b = random.randint(150,255)
                g = random.randint(150,255)
                r = random.randint(200,255)
                if single_plane:
                    for plane in inv_z_planes:
                        plane = plane[:,:,:2]
                        plane = plane.reshape((-1,1,2))
                        cv2.polylines(img,np.int32([plane]),True,(150,0,255),2)
                else:
                    for plane in inv_z_planes:
                        plane = plane[:,0:2].reshape((-1,1,2))
                        cv2.polylines(img,np.int32([plane]),True,(150,0,255),2)

                cv2.putText(img, "{}".format(output_points[i]), (pt[0] + 5,pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (b,g,r), 2)
                cv2.circle(img,(pt[0],pt[1]),4,(b,g,r),-2)
                cv2.imshow("result", img)
                key = cv2.waitKey(1000)
                img = np.copy(img_r)
                if key == ord('q'):
                    run = False
                    break
    cv2.destroyAllWindows()