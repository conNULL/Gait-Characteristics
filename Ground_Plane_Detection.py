from Gait_Analysis_Utils import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.linalg as spl

def getWalkingDirection(methodState, doPlot = False):
    
    '''
    Detects walking direction based on motion of shoulders, similar to what was proposed by 
    "People tracking with body pose estimation for human path prediction"
    
    Returns a numpy array [x,y,z] representing the vector of the direction of walking
    '''
    
    data = methodState.allData
    zenoData = methodState.zenoData
    
    filter = getMeanKernel(3)
    
    leftShoulderPosition = getFilteredPosition("Left Shoulder", filter, data)
    rightShoulderPosition = getFilteredPosition("Right Shoulder", filter, data)
    
    averageShoulderPosition = np.add(leftShoulderPosition, rightShoulderPosition)/2
    
    averageShoulderDiff = np.diff(averageShoulderPosition,axis=0)
    
    walkingDirection = np.mean(averageShoulderDiff,axis=0)
    
    if doPlot:
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        a = np.zeros([averageShoulderDiff.shape[0]])
        ax.quiver(a,a,a,averageShoulderDiff[:,0],averageShoulderDiff[:,1],averageShoulderDiff[:,2],length=0.3,arrow_length_ratio=0.1)
        ax.quiver([0],[0],[0], walkingDirection[0],walkingDirection[1],walkingDirection[2],length=2,arrow_length_ratio=0.5)
        plt.show()
    return walkingDirection/np.linalg.norm(walkingDirection)
  
def calculateGroundPlaneEquation(leftHeelPositions, rightHeelPositions, leftToePositions, rightToePositions):
    
    
    allGroundPoints = np.concatenate([leftHeelPositions,rightHeelPositions,leftToePositions,rightToePositions])
    normal,_,_,_ = spl.lstsq(np.c_[allGroundPoints[:,0],allGroundPoints[:,1], np.ones(allGroundPoints.shape[0])],allGroundPoints[:,2])
    
    # normal = normal/np.linalg.norm(normal)
    
    return normal, allGroundPoints
    
def getGroundPlaneEquation(methodState, doPlot=False):
    
    '''
    
    Detects the ground plane using the location of feet during steps.
    
    Returns a numpy array [a,b,c,d] where elements are the contants in the equation
    of the ground plane ax+by+cz+d = 0
    '''
    
    leftHeelPositions, rightHeelPositions, leftToePositions,rightToePositions= methodState.stepPositionFunction(methodState)
    
    normal, allGroundPoints = calculateGroundPlaneEquation(leftHeelPositions, rightHeelPositions, leftToePositions,rightToePositions)
    
    if doPlot:
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.scatter(allGroundPoints[:,0],allGroundPoints[:,1],allGroundPoints[:,2])
        
        X,Y = np.meshgrid(np.arange(np.min(allGroundPoints[:,0])-1, np.max(allGroundPoints[:,0])+1, 0.1), np.arange(np.min(allGroundPoints[:,1])-1,np.max(allGroundPoints[:,1])+1, 0.1))
        
        Z = normal[0]*X + normal[1]*Y + normal[2]
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.2)
        
        plt.show()
    return np.array([normal[0], normal[1], -1, normal[2]])