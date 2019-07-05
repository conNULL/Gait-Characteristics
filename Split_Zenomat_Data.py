import re

FILENAME = "ZedCam Test 02.csv"

f = open(FILENAME, "r")
lines = [line.split(',') for line in f.readlines()]
f.close()

name = lines[0][1].lower().replace(" ", "") + "_Zeno.csv"
columns = lines[3][2:55]

f = open(name, "w")

numeric = re.compile("[0-9]+\.*[0-9]*")
f.write("Foot"+",")
for col in columns:
    
    f.write(col + ",")
f.write(",\n")
for line in lines[1:]:
    if line[0] == "Memo":
        f.close()
        
        name = line[1].replace(" ","").lower().replace(" ", "") + "_Zeno.csv"
        f = open(name, "w")
        f.write("Foot"+",")
        for col in columns:
            
            f.write(col + ",")
        f.write(",\n")
        
    elif line[0].isnumeric():
        f.write(line[1] + ",")
        for e in line[2:]:
            if numeric.search(e) != None:
                f.write(e + ",")
            else:
                f.write("0,")
        f.write("\n")
                
f.close()