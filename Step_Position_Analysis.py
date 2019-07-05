from Gait_Analysis_Utils import *

def getStepPositions(methodState):
    '''
    
    Calculates Step Positions by taking the positions of the toe and heel at calculated step times
    Error is not estimated here, as it is not possible to find an upper bound on absolute step positions without and point of calibration with the Zeno mat. 
    The error on the actual positions is not important as it does not necessarily influence error on and gait characteristics of interest.
    '''
    
    data = methodState.allData
    zenoData = methodState.zenoData
    
    relativeStepTimes, absoluteStepTimes, error,_,_,_ = methodState.timeFunc(methodState)
    
    stepData = data.loc[data["Time Stamp"].isin(absoluteStepTimes)]
    
    zHeelPositions = np.transpose(np.array([getColumn("Foot Heel X Location (cm.)",zenoData) ,getColumn("Foot Heel Y Location (cm.)",zenoData)]))       
    zToePositions = np.transpose(np.array([getColumn("Foot Toe X Location (cm.)",zenoData) ,getColumn("Foot Toe Y Location (cm.)",zenoData)]))	
    
    filter = getMeanKernel(1)
    
    
    leftHeelPositions = getFilteredPosition("Left Heel", filter,stepData)
    rightHeelPositions = getFilteredPosition("Right Heel", filter, stepData)
    leftToePositions = getFilteredPosition("Left Big Toe", filter, stepData)
    rightToePositions = getFilteredPosition("Right Big Toe", filter, stepData)
    
    
    return leftHeelPositions,rightHeelPositions,leftToePositions,rightToePositions
    
    
def getStepSequence(leftPositions, rightPositions, methodState):
    
    secondStep, firstStep = getLaterPoint(rightPositions[0], leftPositions[0], methodState.walkingDirection)
    
    allPositions = []
    if np.array_equal(secondStep,rightPositions[0]):
        
        for i in range(0,len(leftPositions)-1,2):
            allPositions.append(rightPositions[i])
            allPositions.append(leftPositions[i+1])
            
        if len(rightPositions) %2 == 1:
            allPositions.append(rightPositions[-1])
            
    else:
        
        for i in range(0,len(rightPositions)-1,2):
            allPositions.append(leftPositions[i])
            allPositions.append(rightPositions[i+1])
            
        if len(rightPositions) %2 == 1:
            allPositions.append(leftPositions[-1])
            
    return allPositions
    
def getStrideAndStepLength(rightPositions,leftPositions, methodState):
    
    '''
    Calculates stride length and step length based on the distance between the given joint positions during detected step times.
    
    Returns:
    -an array of stride lengths
    -an array of step lengths
    -an array of stride length errors
    -an array of step length errors
    '''
    
    zStrideLength = getColumn("Stride Length (cm.)", methodState.zenoData)    
    zStepLength = getColumn("Absolute Step Length (cm.)",  methodState.zenoData)
    
    
    allPositions = getStepSequence(rightPositions,leftPositions, methodState)
    
    strideLengths = []
    strideLengthErrors = []
    
    for i in range(len(zStrideLength)):
        
        if zStrideLength[i] != 0:
            stride = np.linalg.norm(np.subtract(allPositions[i+2],allPositions[i]))
            strideLengths.append(stride)
            strideLengthErrors.append(stride - zStrideLength[i])
        
    stepLengths = []
    stepLengthErrors = []
    
    for i in range(len(zStepLength)):
        
        
        if zStepLength[i] != 0:
            step = np.linalg.norm(np.subtract(allPositions[i+1],allPositions[i]))
            stepLengths.append(step)
            stepLengthErrors.append(step - zStepLength[i])
        
        
        
        
    return strideLengths, stepLengths, strideLengthErrors, stepLengthErrors
    
def getHeelStrideAndStepLength(methodState):
    
    '''
    Calculates stride length and step length based on the distance between heel positions during detected step times.
    
    Returns:
    -an array of stride lengths
    -an array of step lengths
    -an array of stride length errors
    -an array of step length errors
    '''
    leftHeelPositions,rightHeelPositions,leftToePositions,rightToePositions = methodState.stepPositionFunction(methodState)
    
    return getStrideAndStepLength(rightHeelPositions, leftHeelPositions, methodState)
        
        
    
    