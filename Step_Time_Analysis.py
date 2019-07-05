from Gait_Analysis_Utils import *
import matplotlib.pyplot as plt
from Gait_Analysis_Method_State import *


def getBestTimes(detectedTimes,referenceTimes):
    
    relativeStepTimes = np.subtract(detectedTimes, detectedTimes[0])
    referenceTimes -= referenceTimes[0]
    
    diffRelativeStepTimes, diffZTimes, diff,offset = alignTimes(np.diff(relativeStepTimes), np.diff(referenceTimes))
    
    relativeStepTimes = np.concatenate([[0], np.cumsum(diffRelativeStepTimes)])    
    referenceTimes = np.concatenate([[0], np.cumsum(diffZTimes)])
    
    error = np.abs(np.subtract(relativeStepTimes[1:], referenceTimes[1:]))
    
    if len(detectedTimes)> offset:
        absoluteStepTimes = relativeStepTimes +detectedTimes[offset]
    else:
        absoluteStepTimes = relativeStepTimes
    
    return relativeStepTimes, absoluteStepTimes, error
    
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
    
    maxTimes = pruneMax(sps.argrelextrema(distance, np.greater)[0], time, distance)
    zTimes = getColumn("First Contact (sec.)", methodState.zenoData)
    
    return getBestTimes(maxTimes, zTimes)
    
def getStepTimesFromHeelToeTimes(methodState):
    
    heelRelativeStepTimes, heelAbsoluteStepTimes, heelError, toeRelativeStepTimes, toeAbsoluteStepTimes, toeError = methodState.heelStrikeToeOffFunction(methodState)
    
    # stepTimes = (heelAbsoluteStepTimes + toeAbsoluteStepTimes)/2
    # 
    # relativeStepTimes = stepTimes - stepTimes[0]
    # stepError = (heelError + toeError)/2
    
    return heelRelativeStepTimes, heelAbsoluteStepTimes, heelError
    
    
    
    
def getHeelToeError(leftHeelTimes,rightHeelTimes, leftToeTimes,rightToeTimes, methodState):
    

    heelTime = getColumn("First Contact (sec.)", methodState.zenoData)
    toeTime = getColumn("Last Contact (sec.)", methodState.zenoData)
    footSequence = getColumn("Foot",methodState.zenoData)
    measuredHeel = [0]
    measuredToe = [0]
    if "Right" in footSequence[0]:
        
        measuredHeel = mergeAlternateSequence(rightHeelTimes, leftHeelTimes)
        measuredToe = mergeAlternateSequence(rightToeTimes, leftToeTimes)
            
            
    else:
        
        
        measuredHeel = mergeAlternateSequence(leftHeelTimes, rightHeelTimes)
        measuredToe = mergeAlternateSequence(leftToeTimes, rightToeTimes)
        
        
    
    heelRelativeStepTimes, heelAbsoluteStepTimes, heelError = getBestTimes(measuredHeel[1:],heelTime)
    toeRelativeStepTimes, toeAbsoluteStepTimes, toeError = getBestTimes(measuredToe[1:],toeTime)
    
    return heelRelativeStepTimes, heelAbsoluteStepTimes, heelError, toeRelativeStepTimes, toeAbsoluteStepTimes, toeError
        
def getHeelStrikeAndToeOffTimesZeni(methodState,butter=False,W=0):
    
    '''
    Calculates times of Heel Strike and Toe Off for each step.
    Method based on "Two simple methods for determining gait events during treadmill and overground walking using kinematic data"
    '''
    ltime = getColumn("Time Stamp", methodState.ldata)
    rtime =  getColumn("Time Stamp", methodState.rdata)
    
    if not butter:
        filter = getMeanKernel(3)
        rmidHip = getFilteredPosition("Mid Hip", filter,methodState.rdata)
        lmidHip = getFilteredPosition("Mid Hip", filter,methodState.ldata)
        leftHeel = getFilteredPosition("Left Heel",  filter,methodState.ldata)
        rightHeel = getFilteredPosition("Right Heel", filter,methodState.rdata)
        leftToe = getFilteredPosition("Left Small Toe",  filter,methodState.ldata)
        rightToe = getFilteredPosition("Right Small Toe",  filter,methodState.rdata)
        ltime2 = ltime
        rtime2 = rtime
    else:
        rmidHip = getButterworthFilteredPosition("Mid Hip", W,methodState.rdata)
        lmidHip = getButterworthFilteredPosition("Mid Hip", W,methodState.ldata)
        leftHeel = getButterworthFilteredPosition("Left Heel",  W,methodState.ldata)
        rightHeel = getButterworthFilteredPosition("Right Heel", W,methodState.rdata)
        leftToe = getButterworthFilteredPosition("Left Small Toe",  W,methodState.ldata)
        rightToe = getButterworthFilteredPosition("Right Small Toe",  W,methodState.rdata)
        ltime2 =getLinearInterpolatedColumn(ltime)
        rtime2 = getLinearInterpolatedColumn(rtime)
        
    
    leftHeelDistance = np.array([getProjectedLength(lmidHip[i], leftHeel[i],methodState.walkingDirection) for i in range(len(lmidHip))])  
    rightHeelDistance = np.array([getProjectedLength(rmidHip[i], rightHeel[i],methodState.walkingDirection) for i in range(len(rmidHip))] )   
    leftToeDistance = np.array([getProjectedLength(lmidHip[i], leftToe[i],methodState.walkingDirection) for i in range(len(lmidHip))]    )
    rightToeDistance =np.array( [getProjectedLength(rmidHip[i], rightToe[i],methodState.walkingDirection) for i in range(len(rmidHip))])
    
    temp =  getHeelToeError(getPrunedDistanceTimes(leftHeelDistance, ltime2, "max"),
    getPrunedDistanceTimes(rightHeelDistance, rtime2, "max"),
    getPrunedDistanceTimes(leftToeDistance, ltime2, "min"),
    getPrunedDistanceTimes(rightToeDistance, rtime2, "min"),
    methodState)
    
    h = temp[1]
    to = temp[4]
    
    limit = -1
    # limit = np.argmax(rightProjectedVelocity>0.002) - 1
    
    if butter:
        if Gait_Analysis_Method_State.cur == 1:
            # Gait_Analysis_Method_State.fig1 = plt.figure()
            plt.subplot(131)
            plt.plot(ltime2[:limit], leftHeelDistance[:limit], label="left heel")    
            plt.plot(rtime2[:limit], rightHeelDistance[:limit], label="right heel")  
            plt.plot(ltime2[:limit], leftToeDistance[:limit], label="left toe")    
            plt.plot(rtime2[:limit], rightToeDistance[:limit], label="right toe")  
            plt.title("Left Camera")
        elif Gait_Analysis_Method_State.cur == 2:
            # Gait_Analysis_Method_State.fig1 = plt.figure()
            plt.subplot(132)
            plt.plot(ltime2[:limit], leftHeelDistance[:limit], label="left heel")    
            plt.plot(rtime2[:limit], rightHeelDistance[:limit], label="right heel")  
            plt.plot(ltime2[:limit], leftToeDistance[:limit], label="left toe")    
            plt.plot(rtime2[:limit], rightToeDistance[:limit], label="right toe")  
            plt.title("Right Camera")
        elif Gait_Analysis_Method_State.cur == 3:
            # Gait_Analysis_Method_State.fig1 = plt.figure()
            plt.subplot(133)
            plt.plot(ltime2[:limit], leftHeelDistance[:limit], label="left heel")    
            plt.plot(rtime2[:limit], rightHeelDistance[:limit], label="right heel")  
            plt.plot(ltime2[:limit], leftToeDistance[:limit], label="left toe")    
            plt.plot(rtime2[:limit], rightToeDistance[:limit], label="right toe")   
            plt.title("Both Cameras")
        
        if Gait_Analysis_Method_State.cur <= 3 and Gait_Analysis_Method_State.cur > 0:

            plt.axvline(x=h[0],label="FS",color="m", linestyle='-',linewidth=0.4)
            plt.axvline(x=to[0],label="TO", color="c", linestyle='-',linewidth=0.4)
            
            for he in h[1:]:
                plt.axvline(x=he,color="m", linestyle='-',linewidth=0.4)
            for toe in to[1:]:
                plt.axvline(x=toe, color="c", linestyle='-',linewidth=0.4)
            plt.xlabel("Time [ms]")
            plt.ylabel("Distance from Hip [m]")
            plt.ylim(-1,1)
            plt.legend(loc="upper left")
            plt.show()
        Gait_Analysis_Method_State.cur += 1
        
    return temp
    
    # print("left heel", time[sps.argrelextrema(leftHeelDistance, np.greater)[0]])    
    # print("right heel", time[sps.argrelextrema(rightHeelDistance, np.greater)[0]])    
    # print("left toe", time[sps.argrelextrema(leftToeDistance, np.greater)[0]])    
    # print("right toe", time[sps.argrelextrema(rightToeDistance, np.greater)[0]])
    # print("heel", heelTime)
    # print("toe", toeTime)
    
# def getHeelStrikeAndToeOffTimesHipExtension(methodState,butter=False,W=0):
#     
#     
#     ltime = getColumn("Time Stamp", methodState.ldata)
#     rtime =  getColumn("Time Stamp", methodState.rdata)
#     
#     if not butter:
#         filter = getMeanKernel(3)
#         rmidHip = getFilteredPosition("Mid Hip", filter,methodState.rdata)
#         lmidHip = getFilteredPosition("Mid Hip", filter,methodState.ldata)
#         rneck = getFilteredPosition("Neck Position", filter,methodState.rdata)
#         lneck = getFilteredPosition("Neck Position", filter,methodState.ldata)
#         leftHip = getFilteredPosition("Left Hip",  filter,methodState.ldata)
#         rightHip = getFilteredPosition("Right Hip", filter,methodState.rdata)
#         leftKnee = getFilteredPosition("Left Knee",  filter,methodState.ldata)
#         rightKnee = getFilteredPosition("Right Knee",  filter,methodState.rdata)
#         ltime2 = ltime
#         rtime2 = rtime
#     else:
#         rmidHip = getButterworthFilteredPosition("Mid Hip", W,methodState.rdata)
#         lmidHip = getButterworthFilteredPosition("Mid Hip", W,methodState.ldata)
#         rneck = getButterworthFilteredPosition("Neck Position", W,methodState.rdata)
#         lneck = getButterworthFilteredPosition("Neck Position", W,methodState.ldata)
#         leftHip = getButterworthFilteredPosition("Left Hip",  W,methodState.ldata)
#         rightHip = getButterworthFilteredPosition("Right Hip", W,methodState.rdata)
#         leftKnee = getButterworthFilteredPosition("Left Knee",  W,methodState.ldata)
#         rightKnee = getButterworthFilteredPosition("Right Knee",  W,methodState.rdata)
#         ltime2 =getLinearInterpolatedColumn(ltime)
#         rtime2 = getLinearInterpolatedColumn(rtime)
#         
#         
#     langles = []
#     rangles = []
#     
#     for i in range(len(ltime)):
#         langles.append(getJointAngle(leftHip[i],leftKnee[i], lmidHip[i], )

def getHeelStrikeAndToeOffTimesVerticalVelocity(methodState,butter=False,W=0):
    
    ltime = getColumn("Time Stamp", methodState.ldata)
    rtime =  getColumn("Time Stamp", methodState.rdata)
    
    if not butter:
        filter = getMeanKernel(3)

        rmidHip = getFilteredPosition("Mid Hip", filter,methodState.rdata)
        lmidHip = getFilteredPosition("Mid Hip", filter,methodState.ldata)
        leftHeel = getFilteredPosition("Left Heel",  filter,methodState.ldata)
        rightHeel = getFilteredPosition("Right Heel", filter,methodState.rdata)
        leftToe = getFilteredPosition("Left Small Toe",  filter,methodState.ldata)
        rightToe = getFilteredPosition("Right Small Toe",  filter,methodState.rdata)
        rneck = getFilteredPosition("Neck", filter,methodState.rdata)
        lneck = getFilteredPosition("Neck", filter,methodState.ldata)
        ltime2 = ltime
        rtime2 = rtime
    else:

        rmidHip = getButterworthFilteredPosition("Mid Hip", W,methodState.rdata)
        lmidHip = getButterworthFilteredPosition("Mid Hip", W,methodState.ldata)
        leftHeel = getButterworthFilteredPosition("Left Heel",  W,methodState.ldata)
        rightHeel = getButterworthFilteredPosition("Right Heel", W,methodState.rdata)
        leftToe = getButterworthFilteredPosition("Left Small Toe",  W,methodState.ldata)
        rightToe = getButterworthFilteredPosition("Right Small Toe",  W,methodState.rdata)
        rneck = getButterworthFilteredPosition("Neck", W,methodState.rdata)
        lneck = getButterworthFilteredPosition("Neck", W,methodState.ldata)
        ltime2 =getLinearInterpolatedColumn(ltime)
        rtime2 = getLinearInterpolatedColumn(rtime)  

        
    
    leftFootPosition = (leftHeel+leftToe)/2
    rightFootPosition = (rightHeel+rightToe)/2
    rightVertical = rneck-rmidHip
    leftVertical = lneck-lmidHip
    
    leftFootVelocity = getDerivative(leftFootPosition,ltime2)
    rightFootVelocity = getDerivative(rightFootPosition, rtime2)
    
    leftProjectedVelocity = []
    rightProjectedVelocity = []
    
    for i in range(len(leftFootVelocity)):
        
        leftProjectedVelocity.append(getProjectedLength(np.zeros([3]), leftFootVelocity[i], leftVertical[i]))
        
    
    for i in range(len(rightFootVelocity)):
        
        rightProjectedVelocity.append(getProjectedLength(np.zeros([3]), rightFootVelocity[i], rightVertical[i]))
    
    leftProjectedVelocity = np.array(leftProjectedVelocity)    
    rightProjectedVelocity = np.array(rightProjectedVelocity)
    
    limit = -1
    # limit = np.argmax(rightProjectedVelocity>0.002) - 1
    
    temp =getHeelToeError(getPrunedDistanceTimes(leftProjectedVelocity, ltime2, "min"),
    getPrunedDistanceTimes(rightProjectedVelocity, rtime2, "min"),
    getPrunedDistanceTimes(leftProjectedVelocity, ltime2, "max"),
    getPrunedDistanceTimes(rightProjectedVelocity, rtime2, "max"),
    methodState)
    
    
    h = temp[1]
    to = temp[4]
    
    if butter:
        if Gait_Analysis_Method_State.cur == 1:
            # Gait_Analysis_Method_State.fig1 = plt.figure()
            plt.subplot(131)
            plt.plot(ltime2[:limit], leftProjectedVelocity[:limit], label="left foot")    
            plt.plot(rtime2[:limit], rightProjectedVelocity[:limit], label="right foot")  
            plt.title("Left Camera")
        elif Gait_Analysis_Method_State.cur == 2:
            # Gait_Analysis_Method_State.fig1 = plt.figure()
            plt.subplot(132)
            plt.plot(ltime2[:limit], leftProjectedVelocity[:limit], label="left foot")    
            plt.plot(rtime2[:limit], rightProjectedVelocity[:limit], label="right foot")  
            plt.title("Right Camera")
        elif Gait_Analysis_Method_State.cur == 3:
            # Gait_Analysis_Method_State.fig1 = plt.figure()
            plt.subplot(133)
            plt.plot(ltime2[:limit], leftProjectedVelocity[:limit], label="left foot")    
            plt.plot(rtime2[:limit], rightProjectedVelocity[:limit], label="right foot")  
            plt.title("Both Camera")

        if Gait_Analysis_Method_State.cur <= 3 and Gait_Analysis_Method_State.cur > 0:

            plt.axvline(x=h[0],label="FS",color="m", linestyle='-',linewidth=0.4)
            plt.axvline(x=to[0],label="TO", color="c", linestyle='-',linewidth=0.4)
            
            for he in h[1:]:
                plt.axvline(x=he,color="m", linestyle='-',linewidth=0.4)
            for toe in to[1:]:
                plt.axvline(x=toe, color="c", linestyle='-',linewidth=0.4)
            plt.xlabel("Time [ms]")
            plt.ylabel("Distance from Hip [m]")
            plt.ylim(-0.004,0.004)
            plt.legend(loc="upper left")
            plt.show()
        Gait_Analysis_Method_State.cur += 1
        
        
    return temp
    
def getButterFilteredStepTime(methodState):
    
    
    heelRelativeStepTimes, heelAbsoluteStepTimes, heelError = getStepTimesFromHeelToeTimes(methodState)
    
    frequency = len(heelRelativeStepTimes)/len(methodState.data)

    
    return methodState.heelStrikeToeOffFunction(methodState,True, 2*frequency)
    
def getNonButterFilteredStepTime(methodState):
    
    
    return methodState.heelStrikeToeOffFunction(methodState)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    