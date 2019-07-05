import json
import numpy as np
import matplotlib.pyplot as plt
import os
import re
from Gait_Analysis_Utils import *

''' 
OpenPose Keypoint Index Reference

0,  "Nose"
1,  "Neck"
2,  "RShoulder"
3,  "RElbow"
4,  "RWrist"
5,  "LShoulder"
6,  "LElbow"
7,  "LWrist"
8,  "MidHip"
9,  "RHip"
10, "RKnee"
11, "RAnkle"
12, "LHip"
13, "LKnee"
14, "LAnkle"
15, "REye"
16, "LEye"
17, "REar"
18, "LEar"
19, "LBigToe"
20, "LSmallToe"
21, "LHeel"
22, "RBigToe"
23, "RSmallToe"
24, "RHeel"
25, "Background"
'''

def writeColumnName(param, outFile):
    
    if "Position" in param:
        outFile.write(param + " x,")
        outFile.write(param + " y,")
        outFile.write(param + " z,")
        outFile.write(param + " confidence,")
    elif "Angle" in param:
        outFile.write(param + ",")
        outFile.write(param + " confidence,")
    else:
        outFile.write(param +",")
        
        
def getKeypoint(index, frame):
    return frame[1+4*index:1+4*(index+1)]
   

    
def getJointAngleParam(p, q, pref, qref, frame):
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
    pJoint = getKeypoint(p, frame)
    qJoint = getKeypoint(q, frame)
    qrefJoint = getKeypoint(qref, frame)
    prefJoint = getKeypoint(pref,frame)
    if frame[0] == 7148:
        print("ok")
    confidence = pJoint[3]*qJoint[3]*qrefJoint[3]*prefJoint[3]
    
    angle = getJointAngle(pJoint[:-1], qJoint[:-1], prefJoint[:-1], qrefJoint[:-1])
    
    return [angle, confidence]

    
    


def getGaitParam(index, gaitParamList, frame):
    
    
    if gaitParamList[index] == "Left Hip Position":
        return getKeypoint(12, frame)
        
    elif gaitParamList[index] == "Right Hip Position":
        return getKeypoint(9, frame)
        
    elif gaitParamList[index] == "Neck Position":
        return getKeypoint(1, frame)
        
    elif gaitParamList[index] == "Left Knee Position":
        return getKeypoint(13, frame)
        
    elif gaitParamList[index] == "Right Knee Position":
        return getKeypoint(10, frame)
        
    elif gaitParamList[index] == "Left Ankle Position":
        return getKeypoint(14, frame)
        
    elif gaitParamList[index] == "Right Ankle Position":
        return getKeypoint(11, frame)
        
    elif gaitParamList[index] == "Left Heel Position":
        return getKeypoint(21, frame)
        
    elif gaitParamList[index] == "Right Heel Position":
        return getKeypoint(24, frame)
        
    elif gaitParamList[index] == "Left Big Toe Position":
        return getKeypoint(19, frame)
        
    elif gaitParamList[index] == "Right Big Toe Position":
        return getKeypoint(22, frame)
        
    elif gaitParamList[index] == "Left Small Toe Position":
        return getKeypoint(20, frame)
        
    elif gaitParamList[index] == "Right Small Toe Position":
        return getKeypoint(23, frame)
        
    elif gaitParamList[index] == "Mid Hip Position":
        return getKeypoint(8, frame)
        
    elif gaitParamList[index] == "Left Shoulder Position":
        return getKeypoint(5, frame)
        
    elif gaitParamList[index] == "Right Shoulder Position":
        return getKeypoint(2, frame)
        
    elif gaitParamList[index] == "Nose Position":
        return getKeypoint(0, frame)
        
    elif gaitParamList[index] == "Left Hip Angle":
        temp =   getJointAngleParam(12, 13, 8, 1, frame)
        temp[0] = 180-temp[0]
        return temp
        
    elif gaitParamList[index] == "Right Hip Angle":
        temp = getJointAngleParam(9, 10, 8, 1, frame)
        temp[0] = 180-temp[0]
        return temp
        
    elif gaitParamList[index] == "Left Knee Angle":
        return getJointAngleParam(13, 14, 13, 12, frame)
        
    elif gaitParamList[index] == "Right Knee Angle":
        return getJointAngleParam(10, 9, 10, 11, frame)
        
    elif gaitParamList[index] == "Left Ankle Angle":
        return getJointAngleParam(21, 19, 14, 13, frame)
        
    elif gaitParamList[index] == "Right Ankle Angle":
        return getJointAngleParam(24, 22, 8, 1, frame)
        
    elif gaitParamList[index] == "Time Stamp":
        return [frame[0]]
        
    else:
        return [0]

def trimToValidFrames(frames, indexesToIgnore):
    
    return frames[1:]
    
if __name__ == "__main__":
    f = open("params.json", 'r')
    params = json.load(f)
    f.close()
    
    dir = params["directory"]
    files = [file for file in os.listdir(dir) if re.search("[12].csv", file) != None]
    # files = ["cforward31.csv"]
    # filename = "S2T31.csv"
    
    for filename in files:
        if "knee" in filename:
            continue
        f = open(dir+filename, 'r')
        frames = [[float(point) if not point == ' -nan(ind)' else 0 for point in frame.split(',')[:-2] ] for frame in f.readlines()[:-2]]
        print(files)
        f.close()
        
        
        GAIT_PARAMS = [
        "Time Stamp",
        "Left Hip Position",
        "Right Hip Position",
        "Left Knee Position",
        "Right Knee Position",
        "Left Ankle Position",
        "Right Ankle Position",
        "Left Heel Position",
        "Right Heel Position",
        "Left Big Toe Position",
        "Right Big Toe Position",
        "Left Small Toe Position",
        "Right Small Toe Position",
        "Mid Hip Position",
        "Neck Position",
        "Left Shoulder Position",
        "Right Shoulder Position",
        "Nose Position",
        "Left Hip Angle",
        "Right Hip Angle",
        "Left Knee Angle",
        "Right Knee Angle",
        "Left Ankle Angle",
        "Right Ankle Angle"
        ]
            
        allOutParams = []
        IRRELEVANT_INDEXES = set([0,1,3,4,6,7,15,16,17,18,25])
            
        frames = trimToValidFrames(frames, IRRELEVANT_INDEXES)
        
        outFile = open(filename[:-4] + "_params.csv", "w")
        for param in GAIT_PARAMS:
            writeColumnName(param, outFile)
        outFile.write("\n")
        
        for frame in frames:
            
            outParams = []
            
            for i in range(len(GAIT_PARAMS)):
                outParams += getGaitParam(i, GAIT_PARAMS, frame)
                
            for param in outParams:
                
                outFile.write(str(param) + ",")
                
            allOutParams.append(outParams)
            outFile.write("\n")
            
        outFile.close()
        
        meank = [1/3,1/3,1/3]
        # meank = [1]
        t = [p[0] for p in allOutParams]        
        ra = [p[-2] for p in allOutParams]        
        rk = [p[-6] for p in allOutParams]        
        rh = [p[-10] for p in allOutParams]
        plt.figure()
        plt.plot(t, np.convolve(meank, ra, mode="same"), label="ankle")
        plt.plot(t, np.convolve(meank, rk, mode="same"), label="knee")
        plt.plot(t, np.convolve(meank, rh, mode="same"), label="hip")
        plt.title(filename)
        plt.xlabel("Time [ms]")
        plt.ylabel("Angle [degrees]")
        plt.legend()
            
        ra = [p[-4] for p in allOutParams]        
        rk = [p[-8] for p in allOutParams]        
        rh = [p[-12] for p in allOutParams]
        plt.figure()
        plt.plot(t, np.convolve(meank, ra, mode="same"), label="ankle")
        plt.plot(t, np.convolve(meank, rk, mode="same"), label="knee")
        plt.plot(t, np.convolve(meank, rh, mode="same"), label="hip")
        plt.xlabel("Time [ms]")
        plt.ylabel("Angle [degrees]")
        plt.title(filename)
        plt.legend()
        plt.show()
    #     
        
        
        
        
        
        
        
        
        