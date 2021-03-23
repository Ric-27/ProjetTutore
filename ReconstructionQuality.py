import numpy as np
import time
import statistics
def numLineasFichero(fichero):
 
    try:
        fichero.seek(0)
        return len(fichero.readlines())
    except AttributeError:
        print("You must insert a file")
        return -1
 
def numLineasFicheroRuta(ruta):
    numLineas = -1
    try:
        fichero = open(ruta, 'r')
        numLineas = len(fichero.readlines())
        fichero.close()
    except AttributeError:
        print("You must insert a file")
    except FileNotFoundError:
        print("The route is incorrect")
    return numLineas
 

inputFile = open('marker/out/Im2XYZ_input.txt', 'r')
nInputFile = numLineasFichero(inputFile)
#allPoints = np.loadtxt('marker/out/Im2XYZ_input.txt')
inputFile.close()
print("Points in the input file: ",nInputFile)

OutputFile = open('marker/out/XYZ_out_filter.txt', 'r')
nOutputFile = numLineasFichero(OutputFile)
#goodPoints = np.loadtxt('marker/out/XYZ_out_filter.txt')
OutputFile.close()
print("Points with 3D coordinates: ",nOutputFile)

#goodPointsPos = np.loadtxt('marker/out/XYZ_out.txt')
#goodPointsPos = np.reshape(goodPointsPos,[len(goodPointsPos),3])
print('3D positions loaded')

quality = (nOutputFile/nInputFile)*100
print("Quality of the reconstruction : ",quality)


badPointsFile = open("badPoints.txt", "w")
i = 0
for x in allPoints:
    x = x.reshape([1,2])
    if i < (goodPoints.shape[0]):
        arrayCompare = x != goodPoints[i]
        if (np.all(arrayCompare[0])):
            np.savetxt(badPointsFile,x)
        else:
            i=i+1
    else:
        np.savetxt(badPointsFile,x)


badPointsFile.close()
badPointsFile = open("badPoints.txt", "r")
nBadPointsFile = numLineasFichero(badPointsFile)
print("Points without coordinates found: ", nBadPointsFile)


