import re

FILENAME = "ZEDCam Walk Trials.csv"

f = open(FILENAME, "r")
lines = [line.split(',') for line in f.readlines()]
f.close()

name = lines[0][1][:4] + "_Zeno.csv"
columns = lines[3][2:55]

f = open(name, "w")

numeric = re.compile("[0-9]+\.*[0-9]*")

for line in lines[1:]:
    if line[0] == "Memo":
        f.close()
        
        name = line[1][:4] + "_Zeno.csv"
        f = open(name, "w")
        for col in columns:
            
            f.write(col + ",")
        f.write(",\n")
        
    elif line[0].isnumeric():
        
        for e in line[2:]:
            if numeric.search(e) != None:
                f.write(e + ",")
            else:
                f.write("0,")
        f.write("\n")
                
f.close()