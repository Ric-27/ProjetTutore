#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 17:44:09 2021

@author: iad

convert csv file containing 3D coordinates pointName and incertitude into micmac Dico-Appuis.xml:
    csv lines are like : x y z name Ix Iy Iz
    with Ix, Iy and Iz incertitude in x, y and z
    exemple :
        10 10.4 10 1012 0.001 0.001 0.005
        1 12.4 10 1015 0.008 0.001 0.005
"""
import xml.etree.ElementTree as ET
import csv
import sys



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

def CSVtoMicmacDicoXML(file_csv, output_directory):
    # read csv and build micmac compatible xml tree 
    Global = ET.Element('Global')
    DicoAppuisFlottant = ET.SubElement(Global, 'DicoAppuisFlottant')
    with open(file_csv, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        for row in reader:
            OneAppuisDAF = ET.SubElement(DicoAppuisFlottant, 'OneAppuisDAF')
            Pt = ET.SubElement(OneAppuisDAF, 'Pt')
            Pt.text = ' '.join(row[0:3])
            NamePt = ET.SubElement(OneAppuisDAF, 'NamePt')
            NamePt.text = row[3]
            Incertitude = ET.SubElement(OneAppuisDAF, 'Incertitude')
            Incertitude.text = ' '.join(row[4:7])
    
    # indent xml to make the file pretty and easier to read (for a human)
    indent(Global)
    # write xml tree into xml file
    tree = ET.ElementTree(Global)
    tree.write(output_directory+'/Dico-Appuis.xml', xml_declaration=True)

if __name__=="__main__":
    # read parameter
    if len(sys.argv) != 3:
        sys.exit("usage : <thisScript.py> <file_csv> <output_directory>")
    file_csv = sys.argv[1]
    output_directory = sys.argv[2]
    # create the micmac Dico-Appuis.xml in the givel directory
    CSVtoMicmacDicoXML(file_csv, output_directory)

