import numpy as np
import time
import statistics

#badPoints = np.loadtxt('badPoints.txt')
badPoints = np.loadtxt('Test_GP.txt')

goodPoints = np.loadtxt('marker/out/XYZ_out_filter.txt')
goodPoints = np.reshape(goodPoints,[len(goodPoints),2])
print('Good points loaded')

goodPointsPos = np.loadtxt('marker/out/XYZ_out.txt')
goodPointsPos = np.reshape(goodPointsPos,[len(goodPointsPos),3])
print('3D positions loaded')

goodPointsList = goodPoints.tolist()
badPointsList = badPoints.tolist()


maxWindow = 2**16
threshold = 10
estimatedPoints = []
start_time = time.time()

estimationFile = open("Estimation_out.txt", "w")
for k,elem in enumerate(badPoints):

    if (badPointsList[k] in goodPointsList):
        print("Point : ", badPoints[k] ," already has 3D coordinates")
        index = goodPointsList.index([badPoints[k][0],badPoints[k][1]])
        print(" 3D coordinates: ", np.reshape(goodPointsPos[index],(1,3)))
        estimatedPoints.append(np.reshape(goodPointsPos[index],(1,3)))
        np.savetxt(estimationFile,np.reshape(goodPointsPos[index],(1,3)))
    else:
        validWindowPoints = []
        validWindowPointsIndex = []
        window = 2

        while(len(validWindowPoints) < threshold and window <= maxWindow):
            i = 0
            while (i <2*window+1):
                j = 0
                while (j <2*window+1):
                    if(i > 0 and i < 2*window and j> 0 and j< 2*window):
                        j = 2*window
                    windowPoint = [float(badPoints[k][0]-window+j), float(badPoints[k][1]-window+i)]
                    if (windowPoint in goodPointsList):
                        if not (windowPoint in validWindowPoints):
                            wpIndex = goodPointsList.index(windowPoint)
                            validWindowPoints.append(windowPoint)
                            validWindowPointsIndex.append(wpIndex)
                    j = j + 1
                i = i + 1
            window = 2 * window
        print("\n Estimated point : ", badPoints[k])
        print("Window Size : ", window)
        print('Points of the window',len(validWindowPointsIndex))
        print("Time taken for the estimation: of this point", time.time()-start_time , "secondes")
        npIndex = np.array(validWindowPointsIndex)
        estimation = np.mean(goodPointsPos[npIndex],0)
        estimation = np.reshape(estimation,(1,3))
        print("3D Estimation : ", estimation)
        estimatedPoints.append(estimation)
        np.savetxt(estimationFile,estimation)
estimationFile.close()

