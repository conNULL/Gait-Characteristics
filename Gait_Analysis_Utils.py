import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sps
import scipy.interpolate as spi

def getDerivative(pos, t):
    
    ret = []
    for i in range(pos.shape[1]):
        ret.append(np.gradient(pos[:,i],t))
        
    return np.array(ret).T
    
def getAngle(p, q, r):
    '''
    
    Calculates the angle between points q and r about point p in the plane formed by p, q, and r.
    
    Params are arrays in the form [x,y,z]
    
    Returns the angle in radians
    '''
    
    pq = np.subtract(q,p)
    pr = np.subtract(r,p)
    
    dot = np.dot(pq,pr)
    normal = np.cross(pq,pr)
    sign = 1
    
    #Note singularity for perfectly horizontal (with respect to camera) limbs
    if normal[2] < 0:
        sign = -1
        
    # det = np.linalg.det((pq,pr,normal))
    # return np.arctan2(det, dot)*180/np.pi
    val =  sign*np.arccos(dot/(np.linalg.norm(pq)*np.linalg.norm(pr)))*180/np.pi
    
    if val > 0:
        val -= 360
        
    return val+180
    
def getJointAngle(p, q, pref, qref):
    '''
    
    Calculates the joint angle for angle p.
    
    Params:
        p is the joint for which to calculate the angle
        q is another end of a limb connected to p
        pref and qref form a limb to form the angle with along with p and q.
        
    
        
    Params are arrays in the form [x,y,z]
    
    Returns the angle in radians
    '''
    p1 = pref
    q1 = np.add(q, np.subtract(pref, p))
    r = qref
    
    return getAngle(p1,q1,r)
    
    
def getLinearInterpolatedColumn(t):
    t2 = [t[0]]
    for i in range(1,len(t)):
        t2.append(np.mean([t[i-1],t[i]]))
        t2.append(t[i])
        
    return np.array(t2)
    
def printError(error, label):

    print(label, "Error:", error, "Mean:", np.mean(error), "Absolute Mean:", np.mean(np.abs(error)), "\n")
    
def getMeanKernel(size):
    
    return [1/size for i in range(size)]
    
def getColumn(colName, data):
    
    if "(cm.)" in colName:
        return np.array(data[colName])/100
    elif "(sec.)" in colName:
        return np.array(data[colName])*1000
        
    return np.array(data[colName])

def getFilteredPosition(joint, kernel, data):
    
    
    x = np.convolve(getColumn(joint +" Position x", data), kernel, mode="same")    
    y = np.convolve(getColumn(joint +" Position y", data), kernel, mode="same")    
    z = np.convolve(getColumn(joint +" Position z", data), kernel, mode="same")
    
    
    return np.array([x,y,z]).T

def getTimedFilteredPosition(joint, kernel, data, stamps):
    
    time = data["Time Stamp"]
    xo = np.convolve(getColumn(joint +" Position x", data), kernel, mode="same")    
    yo = np.convolve(getColumn(joint +" Position y", data), kernel, mode="same")    
    zo = np.convolve(getColumn(joint +" Position z", data), kernel, mode="same")
    
    x = np.interp(stamps,time, xo)    
    y = np.interp(stamps,time, yo)    
    z = np.interp(stamps,time, zo)
    
    return np.array([x,y,z]).T
def getButterworthFilteredPosition(joint, W, data, order=2, interpolate=False):
    
    # interpolate = False
    interpolate = True
    
    kernel = getMeanKernel(1)
    x = np.convolve(getColumn(joint +" Position x", data), kernel, mode="same")    
    y = np.convolve(getColumn(joint +" Position y", data), kernel, mode="same")    
    z = np.convolve(getColumn(joint +" Position z", data), kernel, mode="same")
    
    b,a = sps.butter(order, [W/10,W],btype="bandpass")
    
    # return np.array([x,y,z]).T
    if not interpolate:
        
        x = sps.lfilter(b,a,x)    
        y = sps.lfilter(b,a,y)    
        z = sps.lfilter(b,a,z)
    else:
    
        t = data["Time Stamp"]
        
        t2 = getLinearInterpolatedColumn(t)
        
        xt = sps.lfilter(b,a,x)    
        yt = sps.lfilter(b,a,y)    
        zt = sps.lfilter(b,a,z)
        
        # xt = x    
        # yt = y    
        # zt = z
        
        xs = spi.CubicSpline(t,xt)  
        ys = spi.CubicSpline(t,yt)  
        zs = spi.CubicSpline(t,zt)
        
        x = xs(t2)
        y = ys(t2)
        z = zs(t2)
    
    
    return np.array([x,y,z]).T

def mergeAlternateSequence(arr1,arr2):
    '''
    Merges arrays featuring elements that alternate between elements from arrays and start with an element from arr1
    '''
    
    i = 0
    j = 0
    out = [0]
    while arr1[i+1] < arr2[j]:
        i += 1
        
    out.append(arr1[i])
    
    while j < len(arr2) or i < len(arr1):
        
        if  i == len(arr1) or (j < len(arr2) and arr2[j] < arr1[i]):
            if arr2[j] > out[-1]:
                out.append(arr2[j])
            j +=1
        elif  j == len(arr2) or (i < len(arr1) and arr1[i] <= arr2[j]):
            if arr1[i] > out[-1]:
                out.append(arr1[i])
            i += 1
            
    return out[1:]
  
def pruneMin(minTimeIndexes,time,distance):
    
    # return time[minTimeIndexes]
    maxTimeIndexes = []
        
    ALPHA = 0.1
    
    for i in range(1, len(minTimeIndexes)):
        
        maxTimeIndexes.append(minTimeIndexes[i-1] + np.argmax(distance[minTimeIndexes[i-1]:minTimeIndexes[i]]))
        
    maxTimeIndexes.append(minTimeIndexes[-1] + np.argmax(distance[minTimeIndexes[-1]:]))
    
    maxDistances = distance[maxTimeIndexes]
    minDistances = distance[minTimeIndexes]
    
    maxDistance = maxDistances[np.argsort(maxDistances)[-3]]
    minDistance = minDistances[np.argsort(minDistances)[3]]
    
    threshold = ALPHA*abs(maxDistance-minDistance)
    
    indexesToKeep = []
    
    for i in range(len(maxTimeIndexes)):
        
        if abs(maxDistances[i] - minDistances[i]) > threshold and time[i] != 0:
            indexesToKeep.append(i)
            
    return time[minTimeIndexes[indexesToKeep]]
    
def pruneMax(maxTimeIndexes, time, distance):

    # ALPHA = 0.1
    # 
    # r = times[-1]-time[1]
    # theta = r*ALPHA
    # theta = 500
    # 
    # newExtrema = [times[0]]
    # 
    # for i in range(1,len(times)):
    #     if times[i] - newExtrema[-1] > theta:
    #         newExtrema.append(times[i])
    #         
    # return time[maxTimeIndexes]
    minTimeIndexes = []
        
    ALPHA = 0.1
    
    for i in range(1, len(maxTimeIndexes)):
        
        minTimeIndexes.append(maxTimeIndexes[i-1] + np.argmin(distance[maxTimeIndexes[i-1]:maxTimeIndexes[i]]))
        
    minTimeIndexes.append(maxTimeIndexes[-1] + np.argmin(distance[maxTimeIndexes[-1]:]))
    
    maxDistances = distance[maxTimeIndexes]
    minDistances = distance[minTimeIndexes]
    
    maxDistance = maxDistances[np.argsort(maxDistances)[-3]]
    minDistance = minDistances[np.argsort(minDistances)[3]]
    
    threshold = ALPHA*(maxDistance-minDistance)
    
    indexesToKeep = []
    
    for i in range(len(maxTimeIndexes)):
        
        if maxDistances[i] - minDistances[i] > threshold and time[i] != 0:
            indexesToKeep.append(i)
            
    return time[maxTimeIndexes[indexesToKeep]]

def getPrunedDistanceTimes(distances, times, func):
    '''
    returns the times at which distances occur, after pruning. Assumes times and distance at every index correspond to each other.
    '''
    
    if func == "max":
        return pruneMax(sps.argrelextrema(distances, np.greater)[0], times, distances)    
    elif func == "min":
        return pruneMin(sps.argrelextrema(distances, np.less)[0], times, distances)
    
def alignTimes(arr1, arr2):
    
    if len(arr1) < len(arr2):
        arr1, arr2 = arr2, arr1
        swapped = True
    else:
        swapped = False
        
    diff = len(arr1)-len(arr2)
    offset = min(range(diff+1), key=lambda i: np.linalg.norm(np.power(np.abs(np.subtract(arr1[i:i+len(arr2)], arr2)),[1/2])))
    
    arr1 = arr1[offset: offset+len(arr2)]
    
    if swapped:
        return arr2, arr1, diff, offset
        
    return arr1, arr2, diff, offset
    
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
    
def getProjectedLength(point1,point2, direction):
    
    diff = np.subtract(point2,point1)
    return np.linalg.norm(diff)*np.dot(diff, direction)/(np.linalg.norm(diff)*np.linalg.norm(direction))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    