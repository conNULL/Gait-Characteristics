import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sps
import re
from Gait_Analysis_Utils import *
from Step_Time_Analysis import *
from Ground_Plane_Detection import *
from Gait_Analysis_Method_State import *


    
if __name__== "__main__":
    
    FILENAME = "S2T11_params.csv"
    
    zenoFileName = re.sub("[12]_params", "_Zeno", FILENAME)
    

    zenoData = pd.read_csv(zenoFileName)
    data = pd.read_csv(FILENAME, delimiter=",")
    
    methodState = Gait_Analysis_Method_State(
    data,
    zenoData,
    stepTimeFunction=getStepTimes,
    stepPositionFunction=getStepPositions,
    stepAndStrideFunction=getHeelStrideAndStepLength
    )

##Global Geometry
    methodState.walkingDirection = getWalkingDirection(methodState)
    methodState.Rwc = getRotationToXAxis(methodState.walkingDirection)
    methodState.groundPlane = getGroundPlaneEquation(methodState)
  
##Step Times
    relativeStepTimes, absoluteStepTimes, timeError = methodState.stepTimeFunction(methodState) 
    printError(timeError, "Step Time")
    
##Step Positions
    leftHeelPositions, rightHeelPositions, leftToePositions,rightToePositions= methodState.stepPositionFunction(methodState)
    heelSequence = getStepSequence(rightHeelPositions, leftHeelPositions)
    toeSequence = getStepSequence(rightToePositions, leftToePositions)
   
##Step Length and Stride Length
    strideLengths,StepLengths, strideLengthError,stepLengthError = methodState.stepAndStrideFunction(methodState)   
    printError(strideLengthError, "Stride Length")
    printError(stepLengthError, "Step Length")
       
    for i in range(len(leftHeelPositions)):
        
        print(np.array([np.matmul(methodState.Rwc, leftHeelPositions[i]),np.matmul(methodState.Rwc, rightHeelPositions[i]),np.matmul(methodState.Rwc, leftToePositions[i]),np.matmul(methodState.Rwc, rightToePositions[i])]))
    
##Dimensions
    
    
     
    
    
    
    