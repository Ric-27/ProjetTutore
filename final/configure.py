#python configure.py -v ../ric_test.mp4
import cv2
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-img", "--image", type=str, help="path to the configuration image", default="reference.jpg")
args = vars(ap.parse_args())

step = 0

red = (0,0,255) #BGR
green = (0,255,0)
blue = (255,0,0)
yellow = (0,255,255)
cyan = (255,255,0)
magenta = (255,0,255)
white = (255,255,255)

font = cv2.FONT_HERSHEY_SIMPLEX
font_size = 0.8
font_thickness = 1

global_coord_updated = False
global_x = 0
global_y = 0

coor_x = None
coor_y = None

key_input = ""
text_input = ""
enter = False

foot_text_line_1 = ""
foot_text_line_2 = ""

pts_src = []
pts_dst = []
pts_planes = []

pts_plane = []
priority_defined = False
plane_done = False
priority = 0

pts_src = [[475,211],[660,247],[1111,322],[915,360],[1163,630],[729,634],[370,638],[162,630],[67,428],[378,360],[233,308]]
pts_dst = [[2.00,0.0],[11.70,10.70],[22.80,21.70],[16.80,24.00],[16.80,32.20],[11.10,32.20],[7.30,32.20],[5.00,32.20],[0.30,27.00],[5.00,24.00],[0.0,21.00]]

index = 0

DESIRED_HEIGHT = 720

img = cv2.imread(args["image"],-1)

scale = DESIRED_HEIGHT/img.shape[0]
scaled_width = int(img.shape[1]*scale)
img = cv2.resize(img, (scaled_width,DESIRED_HEIGHT), interpolation = cv2.INTER_AREA)

text_banner = np.ones((80, scaled_width, 3),np.uint8)

img = np.concatenate((img,text_banner),axis=0)
no_text_img = np.copy(img)

def click(event, x, y, flags, param):
    global global_x,global_y,global_coord_updated
    if event == cv2.EVENT_LBUTTONDOWN:
        global_x = x
        global_y = y
        global_coord_updated = True

cv2.namedWindow("Configuration")
cv2.setMouseCallback("Configuration", click)

foot_text_line_1 = "Click to define the points of reference for the top down view (min 4)"

while True:
    key = cv2.waitKey(5)
    if key == ord("c"):
        key_input = "C"
    elif key == ord("n"):
        key_input = "N"
    elif key == ord("p"):
        key_input = "P"
    elif key == ord("q"):
        key_input = "Q"
    elif key == ord("1"):
        key_input = "1"
    elif key == ord("2"):
        key_input = "2"
    elif key == ord("3"):
        key_input = "3"
    elif key == ord("4"):
        key_input = "4"
    elif key == ord("5"):
        key_input = "5"
    elif key == ord("6"):
        key_input = "6"
    elif key == ord("7"):
        key_input = "7"
    elif key == ord("8"):
        key_input = "8"
    elif key == ord("9"):
        key_input = "9"
    elif key == ord("\r"):
        #step = 2
        enter = True
    elif key == 27: #enter
        break
    elif key == -1:
        pass
    else:
        print("Key not recognized")

    if step == 0:
        if len(pts_src) >= 4 and enter:
            enter = False
            step = 1
        elif enter:
            enter = False
        elif len(pts_src) >= 4:
            foot_text_line_2 = "Press enter to advance when done"
        if global_coord_updated:
            pts_src.append([global_x,global_y])
            global_coord_updated = False

    elif step == 1:
        foot_text_line_1 = "Input the coordinates (in meters) of the highlighted point, press enter to advance"
        foot_text_line_2 = "c to clear, p to place decimal point, n for negatives"
        #modify to skip
        if len(pts_dst) == len(pts_src):
            step = 3
        else:
            step = 2
            pts_dst = []

    elif step == 2:        
        if text_input == "" and key_input == 'N':
            text_input = '-'
        elif key_input == 'C':
            text_input = ""
        elif key_input == 'P' and (text_input != "" or text_input != "-"):
            text_input = text_input + "."
        elif key_input == '0' or key_input == '1' or key_input == '2' or key_input == '3' or key_input == '4' or key_input == '5' or key_input == '6' or key_input == '7' or key_input == '8' or key_input == '9':
            text_input = text_input + key_input
        elif key == -1 or enter:
            pass
        else:
            print("Key not recognized")

        if enter:
            if text_input == "" or text_input == "-":
                pass
            elif coor_x is None:
                coor_x = float(text_input)
                text_input = ""
            elif coor_y is None:
                coor_y = float(text_input)
                pts_dst.append([coor_x,coor_y])
                text_input = ""
                coor_x = None
                coor_y = None
                index += 1
        if index >= len(pts_src):
            step = 3
        
    elif step == 3:
        foot_text_line_1 = "Select the points of a work plane (min 3), when done press enter to indicate the z level"
        foot_text_line_2 = "Press enter again to define another plane or q to finish. (c to clear the priority)"

        pts_src = np.array(pts_src)
        pts_src = np.concatenate((pts_src,np.zeros((pts_src.shape[0],1),np.int32)),axis=1)
        pts_dst = np.array(pts_dst)*100
        pts_dst = pts_dst.astype('int32')
        pts_dst = np.concatenate((pts_dst,np.zeros((pts_dst.shape[0],1),np.int32)),axis=1)
        
        window_width = max(pts_dst[:,0])
        window_height = max(pts_dst[:,1])
        h, status = cv2.findHomography(pts_src, pts_dst)
        img = cv2.warpPerspective(img, h, (window_width,window_height))
        
        scale = DESIRED_HEIGHT/img.shape[0]
        scaled_width = int(img.shape[1]*scale)
        
        #pts_dst = (pts_dst*scale).astype(int)

        #img = imutils.resize(img, height = DESIRED_HEIGHT)
        img = cv2.resize(img, (scaled_width,DESIRED_HEIGHT), interpolation = cv2.INTER_AREA)
        text_banner = np.ones((80, scaled_width, 3),np.uint8)
        img = np.concatenate((img,text_banner),axis=0)
        no_text_img = np.copy(img)
        no_text_img = np.copy(img)
        
        step = 4
    
    elif step == 4:
        if key_input == 'Q':
            pts_planes = np.array(pts_planes, dtype=object)
            step = 5
        if plane_done:
            if key_input == 'C':
                text_input = ""
            elif key_input == '0' or key_input == '1' or key_input == '2' or key_input == '3' or key_input == '4' or key_input == '5' or key_input == '6' or key_input == '7' or key_input == '8' or key_input == '9':
                text_input = text_input + key_input
            elif key == -1 or enter:
                pass
            else:
                print("Key not recognized")

        if enter:
            enter = False
            if text_input != "" and plane_done and priority_defined == False:
                priority = int(text_input)
                priority_defined = True
            if priority_defined:
                pts_plane = np.array(pts_plane, dtype=np.int32)
                pts_plane = np.concatenate((pts_plane,priority*np.ones((pts_plane.shape[0],1),np.int32)),axis=1)
                pts_planes.append(pts_plane)

                pts_plane = []
                text_input = ""
                plane_done = False
                priority_defined = False

                print("Plane Saved")

            if len(pts_plane) >= 3:
                plane_done = True
        if global_coord_updated:
            pts_plane.append([global_x,global_y])
            global_coord_updated = False




    elif step == 5:
        print("information saved")
        foot_text_line_1 = "Information Saved"
        foot_text_line_2 = "Press esc to exit"
        np.savez('data', scale = scale, DESIRED_HEIGHT = DESIRED_HEIGHT, pts_src = pts_src, pts_dst = pts_dst, pts_planes = pts_planes)
        step = 6
    
    elif step == 6:
        pass
    
    #draw
    
    if step == 0:
        for pt in pts_src:
            cv2.circle(img,(pt[0],pt[1]),4,yellow,2)

    elif step == 2:
        for id,pt in enumerate(pts_src,0):
            if id == index:
                if text_input == "" and coor_x is None:
                    img_text = "(_,?)"
                elif text_input != "" and coor_x is None and coor_y is None:
                    img_text = "({}_,?)".format(text_input)
                elif coor_x is not None and coor_y is None:
                    img_text = "({},{}_)".format(coor_x,text_input)
                cv2.putText(img, img_text, (pt[0] + 5,pt[1]), font, 1, yellow, 2)  
                cv2.circle(img,(pt[0],pt[1]),4,yellow,2)
            elif id < index:
                cv2.circle(img,(pt[0],pt[1]),4,green,-2)
            else:
                cv2.circle(img,(pt[0],pt[1]),4,red,2)

    elif step == 4:
        if len(pts_planes) > 0:
            pts_planes_np = np.array(pts_planes, dtype = object)
            for plane in pts_planes:
                pts_plane_draw = plane[:,:2].reshape((-1,1,2))
                cv2.polylines(img,np.int32([pts_plane_draw]),True,blue,1)

        if len(pts_plane) > 0:
            pts_plane_np = np.array(pts_plane)
            pts_plane_draw = pts_plane_np[:,:].reshape((-1,1,2))
            if plane_done == False:
                cv2.polylines(img,np.int32([pts_plane_draw]),True,(255,100,100),2)
                for pt in pts_plane_np:
                    cv2.circle(img,(pt[0],pt[1]),4,cyan,-2)
            else:
                cv2.polylines(img,np.int32([pts_plane_draw]),True,green,2)
                (x,y),radius = cv2.minEnclosingCircle(pts_plane_draw)
                if text_input == "":
                    img_text = "Priority:?"
                else:
                    img_text = "Priority:{}".format(text_input)
                cv2.putText(img, img_text, (int(x - radius + 5),int(y)), font, font_size, yellow, 2)
    
    elif step == 6:
        for plane in pts_planes:
            pts_plane_draw = plane[:,:2].reshape((-1,1,2))
            cv2.polylines(img,np.int32([pts_plane_draw]),True,red,2)
    
    while cv2.getTextSize(foot_text_line_1, font, font_size, font_thickness)[0][0] > scaled_width - 10:
        font_size -= 0.005        

    cv2.putText(img, foot_text_line_1, (10, DESIRED_HEIGHT + 30), font, font_size, white, font_thickness)
    cv2.putText(img, foot_text_line_2, (10, DESIRED_HEIGHT + cv2.getTextSize(foot_text_line_1, font, font_size, font_thickness)[0][1] + 40), font, font_size, white, font_thickness)

    cv2.imshow("Configuration", img)
    img = np.copy(no_text_img)
    
    enter = False
    key_input = ""
    global_coord_updated = False
    font_size = 1

cv2.destroyAllWindows()