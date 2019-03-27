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
    stepPositionFunction=getStepPositions
    )
    
    relativeStepTimes, absoluteStepTimes, error = getStepTimes(methodState)          
       
    
    methodState.groundPlane = getGroundPlaneEquation(methodState)
    methodState.walkingDirection = getWalkingDirection(methodState)
    
     
    
    
    
    
    
    
	