import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sps
import re

def getColumn(colName, data):
    
    return np.array(data[colName])

def getFilteredPosition(joint, kernel, data):
    
    x = np.convolve(getColumn(joint +" Position x", data), kernel, mode="same")    
    y = np.convolve(getColumn(joint +" Position y", data), kernel, mode="same")    
    z = np.convolve(getColumn(joint +" Position z", data), kernel, mode="same")
    
    return np.array([x,y,z]).T

def pruneExtrema(times):
    
        # ALPHA = 0.1
        # 
        # r = times[-1]-time[1]
        # theta = r*ALPHA
        theta = 500
        
        newExtrema = [times[0]]
        
        for i in range(1,len(times)):
            if times[i] - newExtrema[-1] > theta:
                newExtrema.append(times[i])
                
        return newExtrema
   
def alignTimes(arr1, arr2):
    
    if len(arr1) < len(arr2):
        arr1, arr2 = arr2, arr1
        swapped = True
    else:
        swapped = False
        
    diff = len(arr1)-len(arr2)
    offset = min(range(diff+1), key=lambda i: np.linalg.norm(np.subtract(arr1[i:i+len(arr2)], arr2)))
    
    arr1 = arr1[offset: offset+len(arr2)]
    
    if swapped:
        return arr2, arr1, diff
        
    return arr1, arr2, diff
    
if __name__== "__main__":
    
    FILENAME = "S2T11_params.csv"
    
    zenoFileName = re.sub("[12]_params", "_Zeno", FILENAME)
    

    zenoData = pd.read_csv(zenoFileName)
    data = pd.read_csv(FILENAME, delimiter=",")
    
    time = getColumn("Time Stamp", data)

    
    filter = [1/5,1/5,1/5,1/5,1/5]
    rightHeel = getFilteredPosition("Right Heel", filter, data)   
    leftHeel = getFilteredPosition("Left Heel", filter, data)   
    
    diff = np.subtract(rightHeel, leftHeel)
    distance = np.linalg.norm(diff, axis=1)
    
    # plt.figure()
    # plt.plot(time, distance)
    # plt.show()
    
    maxTimes = pruneExtrema(time[sps.argrelextrema(distance, np.greater)[0]])
    zenoTimes = getColumn("First Contact (sec.)", zenoData)*1000
    
    maxTimes -= maxTimes[0]
    zenoTimes -= zenoTimes[0]
    
    maxTimes, zenoTimes, diff = alignTimes(maxTimes, zenoTimes)
    
    error = np.abs(np.subtract(maxTimes, zenoTimes))
    meanError = np.mean(error)
    print(error, meanError)