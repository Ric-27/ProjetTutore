#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 16:36:43 2021

@author: iad
"""

import numpy as np
import open3d as o3d
import sys

if len(sys.argv) > 1:
    # read .ply file names and path from the command line arguments
    input_file_list = []
    for i in range(1,len(sys.argv)):
        input_file = sys.argv[i]        
        input_file_list.append(input_file)
else:
    input_file_list = []
    
    #input_file_list.append("dino/dinoDataset/AperiCloud_Arbitrary.ply")
    #input_file_list.append("dino/dinoDataset/d1h1_left.ply")
    
    input_file_list.append("dino/dinoDataset/AperiCloud_Freestyle.ply")
    input_file_list.append("dino/dinoDataset/d2_freestyle_5.ply")
    
    #input_file_list.append("tourou/tourou2/AperiCloud_Tourou2.ply")
    #input_file_list.append("tourou/tourou2/C3DC_BigMac.ply")
    
    #input_file_list.append("plante/AperiCloud_planteA.ply")
    #input_file_list.append("plante/planteA02.ply")
    
# convert ply files into python variables and display it
for fileName in input_file_list:
    # Read the point cloud
    pcd = o3d.io.read_point_cloud(fileName)
    # Visualize the point cloud within open3d
    print('ply fileName =', fileName)
    o3d.visualization.draw_geometries([pcd])
    # Convert open3d format to numpy array
    # Here, you have the point cloud in numpy format. 
    point_cloud_in_numpy = np.asarray(pcd.points)
    
'''
pcdtest = o3d.geometry.PointCloud()
pcdtest.points = o3d.utility.Vector3dVector(point_cloud_in_numpy[0:800000,:])
o3d.visualization.draw_geometries([pcdtest])
'''