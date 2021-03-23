************************
ReconstructionQuality.py
************************

To execute put in terminal:

python3 script/ReconstructionQuality.py

Description:

Reads the number of lines in the input file and the output file of the micmac command Im2XYZ, to calculate the percentage of points that have a 3D coordinate associated. The program also saves an output file "badPoints.txt" with all the pixels that do not have a 3D coordinate associated.


**************************
Im2XYZ_input_generator.cpp
**************************

To compile:

g++ Im2XYZ_input_generator.cpp -o xyz_input_generator.out

To execute(after compilation):

./xyz_input_generator.out $master_height $master_width

where master_height and master_width correspond to the dimensions of the master image.

Description:
Reads the dimensions of the image and generates and output file "Im2XYZ_input.txt" with all the pixels as needed for the Im2XYZ micmac function


****************
EstimationXYZ.py
****************

To execute:

python3 EstimationXYZ.py

Description:

Loads the output files of the Im2XYZ micmac function. Reads a .txt file with the points for which we want to obtain the 3D coordinates, first checks if this point already has these coordinates, and saves them in an output file "Estimation_out.txt". If the coordinates are not available, it estimates them by analyzing the points around the pixel of interest.
The estimation is done by going through the points that are at a 'window' distance from the pixel of interest, and verifying if they have 3D coordinates, if so, the point is saved in a 'validWindowPoints' list. If at the end of the window analysis, the list has more points than a threshold, the program calculates the average of the coordinates within the list to assign that value to the point of interest.

