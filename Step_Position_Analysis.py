from Gait_Analysis_Utils import *

def getStepPositions(methodState):
    '''
    
    Calculates Step Positions by taking the positions of the toe and heel at calculated step times
    Error is not estimated here, as it is not possible to find an upper bound on absolute step positions without and point of calibration with the Zeno mat. 
    The error on the actual positions is not important as it does not necessarily influence error on and gait characteristics of interest.
    '''
    
    data = methodState.data
    zenoData = methodState.zenoData
    
    relativeStepTimes, absoluteStepTimes, error = methodState.stepTimeFunction(methodState)
    
    stepData = data.loc[data["Time Stamp"].isin(absoluteStepTimes)]
    
    zHeelPositions = np.transpose(np.array([getColumn("Foot Heel X Location (cm.)",zenoData) ,getColumn("Foot Heel Y Location (cm.)",zenoData)]))       
    zToePositions = np.transpose(np.array([getColumn("Foot Toe X Location (cm.)",zenoData) ,getColumn("Foot Toe Y Location (cm.)",zenoData)]))	
    
    filter = getMeanKernel(1)
    
    
    leftHeelPositions = getFilteredPosition("Left Heel", filter,stepData)
    rightHeelPositions = getFilteredPosition("Right Heel", filter, stepData)
    leftToePositions = getFilteredPosition("Left Big Toe", filter, stepData)
    rightToePositions = getFilteredPosition("Right Big Toe", filter, stepData)
    
    
    return leftHeelPositions,rightHeelPositions,leftToePositions,rightToePositions
    
    