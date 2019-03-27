import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sps

def getMeanKernel(size):
    
    return [1/size for i in range(size)]
    
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
    
def projectPointToPlane(point, plane):
    
    dist = np.dot(point, plane[:3]) +plane[3]
    
    if dist > 0:
        projectedPoint = point - dist*plane[:3]
    else:
        projectedPoint = point + dist*plane[:3]
        
    return projectedPoint