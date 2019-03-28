from Step_Time_Analysis import *
from Step_Position_Analysis import *
from Ground_Plane_Detection import *
from Gait_Analysis_Utils import *

class Gait_Analysis_Method_State():
    
    def __init__(self,data,zenoData,stepTimeFunction=None,stepPositionFunction=None,stepAndStrideFunction=None,groundPlane=None,walkingDirection=None, Rwc=None, timePruneFunction=None):
        
        self.data = data
        self.zenoData = zenoData
        self.stepTimeFunction = stepTimeFunction
        self.stepPositionFunction = stepPositionFunction
        self.stepAndStrideFunction = stepAndStrideFunction
        self.groundPlane = groundPlane
        self.walkingDirection = walkingDirection
        self.Rwc = Rwc #rotation matrix from walking direction to camera x-axis
        self.timePruneFunction = timePruneFunction