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

def getJointAngleParam(pJoint, qJoint, prefJoint, qrefJoint):
    '''
    
    Calculates the joint angle for angle p with confidence score
    
    Params: indexes for joints where
        p is the joint for which to calculate the angle
        q is another end of a limb connected to p
        pref and qref form a limb to form the angle with along with p and q.
        frame is the state of all keypoints at some point in time
    
        
    Params are arrays in the form [x,y,z]
    
    Returns a list with the angle in radians and confidence score
    '''
    ret = []
    
    for i in range(len(pJoint)):
    
        angle = getJointAngle(pJoint[i], qJoint[i], prefJoint[i], qrefJoint[i])
        
        ret.append(angle)
    
    return np.array(ret)

warnings.filterwarnings("ignore")


if __name__== "__main__":
    
    files = ["back1"]
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
       
        rdata = pd.read_csv(R_FILENAME, delimiter=",").replace(0, np.nan).interpolate()
        ldata = pd.read_csv(L_FILENAME,delimiter=",").replace(0, np.nan).interpolate()
        positionKernel = getMeanKernel(5)
        angleKernel = getMeanKernel(1)
        
        ltime = getColumn("Time Stamp", ldata)      
        rtime = getColumn("Time Stamp", rdata)
        
        if len(ltime) < len(rtime):
            
            frameTime = (ltime[-1] - ltime[0])/len(ltime)
            stamps = np.array([ltime[0] + frameTime*i for i in range(len(ltime)-2)])
            
        else:
            
            frameTime = (rtime[-1] - rtime[0])/len(rtime)
            stamps = np.array([rtime[0] + frameTime*i for i in range(len(rtime)-2)])
            
        
        rneck = getTimedFilteredPosition("Neck", positionKernel, rdata, stamps)        
        lneck = getTimedFilteredPosition("Neck", positionKernel, ldata, stamps)
        
        rmhip = getTimedFilteredPosition("Mid Hip", positionKernel, rdata, stamps)        
        lmhip = getTimedFilteredPosition("Mid Hip", positionKernel, ldata, stamps)
        
        rrhip = getTimedFilteredPosition("Right Hip", positionKernel, rdata, stamps)        
        lrhip = getTimedFilteredPosition("Right Hip", positionKernel, ldata, stamps)
        
        rlhip = getTimedFilteredPosition("Left Hip", positionKernel, rdata, stamps)        
        llhip = getTimedFilteredPosition("Left Hip", positionKernel, ldata, stamps)
        
        rrknee = getTimedFilteredPosition("Right Knee", positionKernel, rdata, stamps)        
        lrknee = getTimedFilteredPosition("Right Knee", positionKernel, ldata, stamps)
        
        rlknee = getTimedFilteredPosition("Left Knee", positionKernel, rdata, stamps)        
        llknee = getTimedFilteredPosition("Left Knee", positionKernel, ldata, stamps)
        
        rrankle = getTimedFilteredPosition("Right Ankle", positionKernel, rdata, stamps)        
        lrankle = getTimedFilteredPosition("Right Ankle", positionKernel, ldata, stamps)
        
        rlankle = getTimedFilteredPosition("Left Ankle", positionKernel, rdata, stamps)        
        llankle = getTimedFilteredPosition("Left Ankle", positionKernel, ldata, stamps)
        
        rrtoe = getTimedFilteredPosition("Right Small Toe", positionKernel, rdata, stamps)        
        lrtoe = getTimedFilteredPosition("Right Small Toe", positionKernel, ldata, stamps)
        
        rltoe = getTimedFilteredPosition("Left Small Toe", positionKernel, rdata, stamps)        
        lltoe = getTimedFilteredPosition("Left Small Toe", positionKernel, ldata, stamps)
        
        rrheel = getTimedFilteredPosition("Right Heel", positionKernel, rdata, stamps)        
        lrheel = getTimedFilteredPosition("Right Heel", positionKernel, ldata, stamps)
        
        rlheel = getTimedFilteredPosition("Left Heel", positionKernel, rdata, stamps)        
        llheel = getTimedFilteredPosition("Left Heel", positionKernel, ldata, stamps)
        
        rrshoulder = getTimedFilteredPosition("Right Shoulder", positionKernel, rdata, stamps)        
        lrshoulder = getTimedFilteredPosition("Right Shoulder", positionKernel, ldata, stamps)
        
        rlshoulder = getTimedFilteredPosition("Left Shoulder", positionKernel, rdata, stamps)        
        llshoulder = getTimedFilteredPosition("Left Shoulder", positionKernel, ldata, stamps)
        
        mmhip = np.mean([lmhip,rmhip], axis=0)
        mmshoulder = np.mean([llshoulder, rrshoulder], axis=0)
        
        rrhipAngle = getJointAngleParam(rrhip, rrknee, rmhip, rneck)
        rrkneeAngle = getJointAngleParam(rrknee, rrankle, rrknee, rrhip)
        rrankleAngle = getJointAngleParam(rrheel, rrtoe, rrankle, rrknee)
        
        
        llhipAngle = getJointAngleParam(llhip, llknee, lmhip, lneck)
        llkneeAngle = getJointAngleParam(llknee, llankle, llknee, llhip)
        llankleAngle = getJointAngleParam(llheel, lltoe, llankle, llknee)
        
        
        s = 100
        e = 300
        t = stamps[s:e]
        plt.figure()
        # plt.plot(t, rrhip[b:e], label="hip")
        # plt.plot(t, rrknee[b:e], label="knee")
        # plt.plot(t, rrshoulder[b:e], label="ankle")
        # plt.plot(t, llshoulder[b:e], label="neck")
    
        W = 0.08
        b,a = sps.butter(2, [W/50, W],btype="bandpass")
        
        
        
        ankle = sps.lfilter(b,a,np.array(pd.DataFrame(-rrankleAngle[s:e]).interpolate()).T)[0]
        knee = sps.lfilter(b,a,np.array(pd.DataFrame(-rrkneeAngle[s:e]).interpolate()).T)[0]
        hip = sps.lfilter(b,a,np.array(pd.DataFrame(rrhipAngle[s:e]).interpolate()).T)[0]
        
        plt.plot(t, np.convolve(angleKernel, ankle, mode="same"), label="ankle")        
        plt.figure()
        plt.plot(t, np.convolve(angleKernel, knee, mode="same"), label="knee")        
        plt.figure()
        plt.plot(t, np.convolve(angleKernel, hip, mode="same"), label="hip")
        
        plt.xlabel("Time [ms]")
        plt.ylabel("Angle [degrees]")
        plt.title("Right")
        plt.legend()
        
        plt.figure()
        ankle = sps.lfilter(b,a,np.array(pd.DataFrame(llankleAngle[s:e]).interpolate()).T)[0]
        knee = sps.lfilter(b,a,np.array(pd.DataFrame(llkneeAngle[s:e]).interpolate()).T)[0]
        hip = sps.lfilter(b,a,np.array(pd.DataFrame(-llhipAngle[s:e]).interpolate()).T)[0]
        plt.plot(t, np.convolve(angleKernel, ankle, mode="same"), label="ankle")        
        plt.figure()
        plt.plot(t, np.convolve(angleKernel, knee, mode="same"), label="knee")        
        plt.figure()
        plt.plot(t, np.convolve(angleKernel, hip, mode="same"), label="hip")
        
        plt.xlabel("Time [ms]")
        plt.ylabel("Angle [degrees]")
        plt.title("Left")
        plt.legend()
    plt.show()
        
        