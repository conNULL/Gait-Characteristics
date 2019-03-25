from Gait_Analysis_Utils import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.linalg as spl

def getGroundPlaneEquation(stepData, doPlot=False):
    
    '''
    
    Detects the ground plane using the location of feet during steps.
    
    Returns a numpy array [a,b,c,d] where elements are the contants in the equation
    of the ground plane ax+by+cz=d
    '''
    
    filter = getMeanKernel(1)
    
    leftHeelPositions = getFilteredPosition("Left Heel", filter,stepData)
    rightHeelPositions = getFilteredPosition("Right Heel", filter, stepData)
    leftToePositions = getFilteredPosition("Left Big Toe", filter, stepData)
    rightToePositions = getFilteredPosition("Right Big Toe", filter, stepData)
    
    allGroundPoints = np.concatenate([leftHeelPositions,rightHeelPositions,leftToePositions,rightToePositions])
    
    if doPlot:
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.scatter(allGroundPoints[:,0],allGroundPoints[:,1],allGroundPoints[:,2])
        
        normal,_,_,_ = spl.lstsq(np.c_[allGroundPoints[:,0],allGroundPoints[:,1], np.ones(allGroundPoints.shape[0])],allGroundPoints[:,2])
        X,Y = np.meshgrid(np.arange(np.min(allGroundPoints[:,0])-1, np.max(allGroundPoints[:,0])+1, 0.1), np.arange(np.min(allGroundPoints[:,1])-1,np.max(allGroundPoints[:,1])+1, 0.1))
        
        Z = normal[0]*X + normal[1]*Y + normal[2]
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.2)
        
        plt.show()
    return np.array([-normal[0], -normal[1], 1, normal[2]])