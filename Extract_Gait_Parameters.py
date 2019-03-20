import json


def getGaitParam(index, gaitParamList, frame):
    
    
    if gaitParamList[index] == "Left Hip Position":
        return frame[49:53]
    elif gaitParamList[index] == "Right Hip Position":
        return frame[37:41]
    else:
        return [0]

def trimToValidFrames(frames, indexesToIgnore):
    
    return frames
    
if __name__ == "__main__":
    f = open("params.json", 'r')
    params = json.load(f)
    f.close()
    
    dir = params["directory"]
    
    filename = "S2T11.csv"
    
    f = open(dir+filename, 'r')
    frames = [[float(point) if not point == ' -nan(ind)' else 0 for point in frame.split(',')[:-2] ] for frame in f.readlines()]
    f.close()
    
    
    GAIT_PARAMS = [
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
    "Mid Hip Position",
    "Left Shoulder Position",
    "Right Shoulder Position",
    "Left Hip Angle",
    "Right Hip Angle",
    "Left Knee Angle",
    "Right Knee Angle",
    "Left Ankle Angle",
    "Right Ankle Angle"
    ]
        
    IRRELEVANT_INDEXES = set([0,1,3,4,6,7,15,16,17,18,25])
        
    frames = trimToValidFrames(frames, IRRELEVANT_INDEXES)
    
    outFile = open(filename[:-4] + "_params.csv", "w")
    
    for frame in frames:
        
        outParams = []
        
        for i in range(len(GAIT_PARAMS)):
            outParams += getGaitParam(i, GAIT_PARAMS, frame)
            
        for param in outParams:
            
            outFile.write(str(param) + ",")
            
        outFile.write("\n")
        
    outFile.close()
        
        
        
        
        
        
        
        
        
        
        
        
        