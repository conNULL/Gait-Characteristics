import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sps

def printError(error, label):

    print(label, "Error:", error, "Mean:", np.mean(error), "Absolute Mean:", np.mean(np.abs(error)), "\n")
    
def getMeanKernel(size):
    
    return [1/size for i in range(size)]
    
def getColumn(colName, data):
    
    if "(cm.)" in colName:
        return np.array(data[colName])/100
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
    
def getLaterPoint(point1,point2,positiveDirection):
    '''
    Given two 3D points and a positive direction, return pointA, pointB where pointA is further in the positive direction than pointB
    '''
    diff = np.subtract(point2,point1)
    angle = np.arccos(np.dot(diff, positiveDirection)/(np.linalg.norm(diff)*np.linalg.norm(positiveDirection)))
    
    if abs(angle) < np.pi/2:
        
        return point2, point1
        
    return point1,point2
    
def getRotationToXAxis(direction):
    
    n_direction = direction/np.linalg.norm(direction)
    x = np.array([1,0,0])
    cross = np.cross(n_direction, x)
    s = np.linalg.norm(cross)
    dot = np.dot(x,n_direction)
    
    skew = np.array([np.array([0,-cross[2], cross[1]]),np.array([cross[2],0, -cross[0]]),np.array([-cross[1],cross[0], 0])])
   
    R = np.identity(3) + skew + np.matmul(skew,skew)/(1+dot)
    
    return R
    
    
    
    
    
    
    
    
    
    
    
    