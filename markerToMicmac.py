import numpy as np
import cv2
from cv2 import aruco
import sys
import glob
import os
import xml.etree.ElementTree as ET


    
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def markers_center(img):
    # frame = cv2.imread("../marker/bedroomMarkerDataset/1_noruller_5.jpg")
    frame = cv2.imread(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    centers = np.zeros([len(ids),2])
    for i in range(len(ids)):
        c = corners[i][0]
        centers[i,:] = [c[:, 0].mean(), c[:, 1].mean()]
    return centers, ids

if __name__=="__main__":
    # read parameter
    if len(sys.argv) < 3:
        sys.exit("error usage : \n<thisScript.py> <image1> ... <imageN> <output_directory>")
    imageList = sys.argv[1:-1]
    output_directory = sys.argv[-1]
    print("extracting markers from images :")
    print('\n'.join(imageList))
    SetOfMesureAppuisFlottants = ET.Element('SetOfMesureAppuisFlottants')
    for img in imageList:
        MesureAppuiFlottant1Im = ET.SubElement(SetOfMesureAppuisFlottants, 'MesureAppuiFlottant1Im')
        NameIm = ET.SubElement(MesureAppuiFlottant1Im, 'NameIm') 
        NameIm.text = os.path.basename(img)
        centers, ids = markers_center(img)    
        for i in range(centers.shape[0]):
            OneMesureAF1I = ET.SubElement(MesureAppuiFlottant1Im, 'OneMesureAF1I')
            NamePt = ET.SubElement(OneMesureAF1I, 'NamePt')
            NamePt.text = str(ids[i,0])
            PtIm = ET.SubElement(OneMesureAF1I, 'PtIm')
            PtIm.text = str(centers[i,0])+' '+str(centers[i,1])
    indent(SetOfMesureAppuisFlottants)
    tree = ET.ElementTree(SetOfMesureAppuisFlottants)
    tree.write(output_directory+'/Mesure-Appuis.xml', xml_declaration=True)

'''
if you don't want to use the terminal

runfile('/home/iad/Documents/ENSTA/3A/projet_tuteure/test/script/markerToMicmac.py',
        wdir='/home/iad/Documents/ENSTA/3A/projet_tuteure/test/script',
        args="'../marker/bedroomMarkerDataset/1_noruller_?.jpg' ./")

debugfile('/home/iad/Documents/ENSTA/3A/projet_tuteure/test/script/markerToMicmac.py',
          wdir='/home/iad/Documents/ENSTA/3A/projet_tuteure/test/script',
          args="'../marker/bedroomMarkerDataset/1_noruller_?.jpg' ./")

'''

