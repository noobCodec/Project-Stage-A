import json
import random

wt_imp = [172, 258, 344, 430, 161, 247, 333, 419, 150, 236, 322, 408, 494, 139, 225, 311, 397, 483, 128, 214, 300, 386, 472, 117, 203, 289, 375, 461, 106, 192]
ht_imp_ft = [12, 13, 5, 6, 14, 15, 12, 4, 5, 13, 14, 15, 3, 7, 4, 12, 13, 15, 2, 7, 16, 13, 14, 6, 15, 3, 16, 13, 5, 14]
ht_imp_in = [6, 7, 3, 4, 8, 9, 8, 4, 5, 9, 10, 11, 5, 7, 6, 10, 11, 0, 6, 9, 1, 0, 1, 10, 2, 9, 3, 2, 11, 3]
ht_met = [381, 414, 160, 193, 447, 480, 386, 132, 165, 419, 452, 485, 104, 231, 137, 391, 424, 457, 76, 236, 490, 396, 429, 208, 462, 114, 495, 401, 180, 434]
wt_met = [78, 117, 156, 195, 73, 112, 151, 190, 68, 107, 146, 185, 224, 63, 102, 141, 180, 219, 58, 97, 136, 175, 214, 53, 92, 131, 170, 209, 48, 87]

def buildJson(system,infile,idx):
    runFile = open("scripts/" + infile, "r+")
    runFileJSON = json.load(runFile)
    if(system[0] == "lb"):
        weight = wt_imp[idx]
    else:
        weight = wt_met[idx]
    if(system[1] == "cm"):
        height = ht_met[idx]
    else:
        height = ht_imp_ft[idx],ht_imp_in[idx]
    age = 18 + idx
    for item in runFileJSON["operations"]["bmi_operation"]:
        if("target_view" in item):
            if(item["target_view"]=="set_weight"):
                item["text"] = weight
            elif(item["target_view"]=="set_age"):
                item["text"] = age
            elif(system[1] == "cm" and item["target_view"]=="set_height"):
                item["text"] = height
            elif(item["target_view"]=="set_height_ft"):
                item["text"] = height[0]
            elif(item["target_view"]=="set_height_in"):
                item["text"] = height[1]
    runFile.close()
    with open("scripts/" + infile, 'w'): pass
    runFile = open("scripts/" + infile,"w+")
    json.dump(runFileJSON, runFile,indent=2)
    if(system[1] == "cm"):
        return f"[cm:{height}||{system[0]}:{weight}||age:{age}"
    else:
        return f"[ft-in:{','.join([str(ht) for ht in height])}||{system[0]}:{weight}||age:{age}"
    