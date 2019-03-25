import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sps
import re
from Gait_Analysis_Utils import *
from Step_Time_Analysis import *


    
if __name__== "__main__":
    
    FILENAME = "S2T11_params.csv"
    
    zenoFileName = re.sub("[12]_params", "_Zeno", FILENAME)
    

    zenoData = pd.read_csv(zenoFileName)
    data = pd.read_csv(FILENAME, delimiter=",")
    
    
    relativeStepTimes, absoluteStepTimes, error = getStepTimes(data, zenoData)
    stepData = data.loc[data["Time Stamp"].isin(absoluteStepTimes)]
    
    zHeelPositions = np.transpose(np.array([getColumn("Foot Heel X Location (cm.)",zenoData) ,getColumn("Foot Heel Y Location (cm.)",zenoData)]))       
    zToePositions = np.transpose(np.array([getColumn("Foot Toe X Location (cm.)",zenoData) ,getColumn("Foot Toe Y Location (cm.)",zenoData)]))   
     
    
    
    
    
    
    
	