from Gait_Analysis_Utils import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.linalg as spl

def getWalkingDirection(methodState):
    
    '''
    Detects walking direction based on motion of shoulders, similar to what was proposed by 
    "People tracking with body pose estimation for human path prediction"
    
    Returns a numpy array [x,y,z] representing the vector of the direction of walking
    '''
    
    data = methodState.data
    zenoData = methodState.zenoData
    
    filter = getMeanKernel(3)
    
    leftShoulderPosition = getFilteredPosition("Left Shoulder", filter, data)
    rightShoulderPosition = getFilteredPosition("Right Shoulder", filter, data)
    
    averageShoulderPosition = np.add(leftShoulderPosition, rightShoulderPosition)/2
    
    averageShoulderDiff = np.diff(averageShoulderPosition,axis=0)
    
    walkingDirection = np.mean(averageShoulderDiff,axis=0)
    
    return walkingDirection/np.linalg.norm(walkingDirection)
  
def calculateGroundPlaneEquation(leftHeelPositions, rightHeelPositions, leftToePositions, rightToePositions):
    
    
    allGroundPoints = np.concatenate([leftHeelPositions,rightHeelPositions,leftToePositions,rightToePositions])
    normal,_,_,_ = spl.lstsq(np.c_[allGroundPoints[:,0],allGroundPoints[:,1], np.ones(allGroundPoints.shape[0])],allGroundPoints[:,2])
    
    normal = normal/np.linalge.norm(normal)
    
    return normal
    
def getGroundPlaneEquation(methodState, doPlot=False):
    
    '''
    
    Detects the ground plane using the location of feet during steps.
    
    Returns a numpy array [a,b,c,d] where elements are the contants in the equation
    of the ground plane ax+by+cz+d = 0
    '''
    
    leftHeelPositions, rightHeelPositions, leftToePositions,rightToePositions= methodState.stepPositionFunction(methodState)
    
    normal = calculateGroundPlaneEquation(leftHeelPositions, rightHeelPositions, leftToePositions,rightToePositions)
    
    if doPlot:
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.scatter(allGroundPoints[:,0],allGroundPoints[:,1],allGroundPoints[:,2])
        
        X,Y = np.meshgrid(np.arange(np.min(allGroundPoints[:,0])-1, np.max(allGroundPoints[:,0])+1, 0.1), np.arange(np.min(allGroundPoints[:,1])-1,np.max(allGroundPoints[:,1])+1, 0.1))
        
        Z = normal[0]*X + normal[1]*Y + normal[2]
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.2)
        
        plt.show()
    return np.array([normal[0], normal[1], -1, normal[2]])