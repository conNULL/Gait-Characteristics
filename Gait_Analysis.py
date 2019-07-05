import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sps
import re
from Gait_Analysis_Utils import *
from Step_Time_Analysis import *
from Ground_Plane_Detection import *
from Gait_Analysis_Method_State import *
import sys
import warnings




warnings.filterwarnings("ignore")


if __name__== "__main__":
    
    files = ["cforward2","cforward3", "Lforward2",  "cback1", "cback2", "Lback2", "Lback3", "Lforward1"]
    lallHeel = []
    lallToe = []
    rallHeel = []
    rallToe = []
    ballHeel = []
    ballToe = []
    # files = ["cforward2"]
    for FILE in files:
        
        
        R_FILENAME = FILE + "1_params.csv"
        L_FILENAME = FILE + "2_params.csv"
        zenoFileName = re.sub("[12]_params", "_Zeno", R_FILENAME)
        
        # print(zenoFileName, "----------------------------")
    
        zenoData = pd.read_csv(zenoFileName)
        rdata = pd.read_csv(R_FILENAME, delimiter=",")
        ldata = pd.read_csv(L_FILENAME,delimiter=",")
        
        methodState = Gait_Analysis_Method_State(
        rdata,
        zenoData,
        stepTimeFunction=getStepTimesFromHeelToeTimes,
        stepPositionFunction=getStepPositions,
        stepAndStrideFunction=getHeelStrideAndStepLength,
        heelStrikeToeOffFunction=getHeelStrikeAndToeOffTimesZeni
        # heelStrikeToeOffFunction=getHeelStrikeAndToeOffTimesVerticalVelocity
        )
        methodState.rdata = rdata
        methodState.ldata = ldata
        methodState.allData = rdata.append(ldata)
        methodState.timeFunc = getButterFilteredStepTime
    
    ##Global Geometry
        methodState.walkingDirection = getWalkingDirection(methodState)
        # raise Exception('exit')
        methodState.Rwc = getRotationToXAxis(methodState.walkingDirection)
        methodState.groundPlane = getGroundPlaneEquation(methodState)
        

        methodState.rdata = ldata
        methodState.ldata = ldata
        heelRelativeStepTimes, heelAbsoluteStepTimes, heelError, toeRelativeStepTimes, toeAbsoluteStepTimes, toeError = methodState.timeFunc(methodState)
        lallHeel.append(np.mean(heelError))
        lallToe.append(np.mean(toeError))
        # print(heelAbsoluteStepTimes)
        # printError(heelError, "Left Heel")        
        # printError(toeError, "Left Toe")
        
        methodState.rdata = rdata
        methodState.ldata = rdata
        heelRelativeStepTimes, heelAbsoluteStepTimes, heelError, toeRelativeStepTimes, toeAbsoluteStepTimes, toeError = methodState.timeFunc(methodState)
        rallHeel.append(np.mean(heelError))
        rallToe.append(np.mean(toeError))
        # print(heelAbsoluteStepTimes)
        # printError(heelError, "Right Heel")        
        # printError(toeError, "Right Toe")

        if "forward" in FILE:
            methodState.rdata = rdata
            methodState.ldata = ldata
        else:
            methodState.rdata = ldata
            methodState.ldata = rdata
            

        heelRelativeStepTimes, heelAbsoluteStepTimes, heelError, toeRelativeStepTimes, toeAbsoluteStepTimes, toeError = methodState.timeFunc(methodState)
        ballHeel.append(np.mean(heelError))
        ballToe.append(np.mean(toeError))
        # print(heelAbsoluteStepTimes)
        # printError(heelError, "Both Heel")        
        # printError(toeError, "Both Toe")
        plt.show()
        # print("heel", heelAbsoluteStepTimes, "relative", heelRelativeStepTimes, "Error",heelError, "Mean", np.mean(heelError) )    
        # print("toe", toeAbsoluteStepTimes, "relative", toeRelativeStepTimes, "Error",toeError, "Mean", np.mean(toeError) )
        # print("heel", np.mean(heelError))
        # print("toe", np.mean(toeError))
        # allHeel.append(np.mean(heelError))
        # allToe.append(np.mean(toeError))
        
    ##Step Times
        # relativeStepTimes, absoluteStepTimes, timeError,_,_,_ = methodState.timeFunc(methodState) 
        # printError(timeError, "Step Time")
        
    ##Step Positions
        # leftHeelPositions, rightHeelPositions, leftToePositions,rightToePositions= methodState.stepPositionFunction(methodState)
        # heelSequence = getStepSequence(rightHeelPositions, leftHeelPositions, methodState)
        # toeSequence = getStepSequence(rightToePositions, leftToePositions, methodState)
        # 
        # if np.array_equal(heelSequence[0], leftHeelPositions[0]):
        #     firstFoot = "left"
        # else:
        #     firstFoot = "right"
    
    ##Step Length and Stride Length
        # strideLengths,StepLengths, strideLengthError,stepLengthError = methodState.stepAndStrideFunction(methodState)   
        # printError(strideLengthError, "Stride Length")
        # printError(stepLengthError, "Step Length")
        
    ##Dimensions
        # 
        # zFootLength = getColumn("Foot Length (cm.)", zenoData)
        # 
        # footLength = np.linalg.norm(np.subtract(toeSequence, heelSequence), axis=1)
        # error = np.subtract(footLength, zFootLength)
        
        # printError(error, "Foot Length")
        
    # print(allHeel)
    # print(allToe)
    print(np.round(np.mean(lallHeel)), np.round(np.std(lallHeel)))
    print(np.round(np.mean(lallToe)), np.round(np.std(lallToe)))
    print(np.round(np.mean(rallHeel)),np.round( np.std(rallHeel)))
    print(np.round(np.mean(rallToe)), np.round(np.std(rallToe)))
    print(np.round(np.mean(ballHeel)), np.round(np.std(ballHeel)))
    print(np.round(np.mean(ballToe)), np.round(np.std(ballToe)))
    