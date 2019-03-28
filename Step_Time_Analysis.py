from Gait_Analysis_Utils import *

def getStepTimes(methodState):
    
    '''
    
    Calculates times of steps based on maximum distance between heels.
    Method based on "Vision-Based Gait Analysis for Senior Care"
    
    '''
    
    time = getColumn("Time Stamp", methodState.data)

    
    filter = getMeanKernel(3)
    rightHeel = getFilteredPosition("Right Heel", filter, methodState.data)   
    leftHeel = getFilteredPosition("Left Heel", filter, methodState.data)   
    
    diff = np.subtract(rightHeel, leftHeel)
    distance = np.linalg.norm(diff, axis=1)
    
    # plt.figure()
    # plt.plot(time, distance)
    # plt.show()
    
    maxTimes = pruneExtrema(sps.argrelextrema(distance, np.greater)[0], time, distance)
    zTimes = getColumn("First Contact (sec.)", methodState.zenoData)*1000
    
    relativeStepTimes = np.subtract(maxTimes, maxTimes[0])
    zTimes -= zTimes[0]
    
    diffRelativeStepTimes, diffZTimes, diff,offset = alignTimes(np.diff(relativeStepTimes), np.diff(zTimes))
    
    relativeStepTimes = np.concatenate([[0], np.cumsum(diffRelativeStepTimes)])    
    zTimes = np.concatenate([[0], np.cumsum(diffZTimes)])
    
    error = np.abs(np.subtract(relativeStepTimes, zTimes))
    
    absoluteStepTimes = np.add(relativeStepTimes, maxTimes[offset])
    
    return relativeStepTimes, absoluteStepTimes, error
    
    
def getHeelStrikeTimes(methodState):
    
    '''
    Calculates times of Heel Strike and Toe Off for each step.
    Method based on "Two simple methods for determining gait events during treadmill and overground walking using kinematic data"
    '''
    
    pass