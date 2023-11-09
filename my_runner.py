import os
import subprocess
import util
import re
import numpy as np
import shutil
import datetime
import json
import time
import multiprocessing as mp
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
whitelist = [file.strip("\n") for file in open("whitelist.txt").readlines()]
a = subprocess.check_output(["adb","devices"])
available_devices = [b.split("\t")[0] for b in a.decode("UTF-8").strip().split("\n")[1:]]
start_tm = time.time()
def run(item,oper_dir,device,idx):
    if(not os.path.exists("run/"+oper_dir)):
        os.makedirs("run/"+ oper_dir)
    if(item == None):
        return
    file = item
    search_file = json.load(open("runtime/"+ file + ".json"))
    code  = [search_file["weight"],search_file["height"]]
    try:
        subprocess.check_call(["adb","-s",device,"shell","pm clear",file])
    except:
        pass
    result = util.buildJson(code,file+".json",idx)
    subprocess.check_call(
        "python3 "
        "./droidbot/start.py -a " + "apks/"+file + ".apk" + " -o ./run/" + oper_dir +" -script ./scripts/" + file+".json"+" -keep_env -keep_app -is_emulator -policy manual"+" -d " + device,shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    state_file = max(
        filter(lambda x: x.endswith("json"), os.listdir("run/" + oper_dir + "/states")),
        key=lambda file: datetime.datetime(int(file[6:10]),int(file[11:13]),int(file[14:16]),int(file[17:19]),int(file[19:21]),int(file[21:23])))
    search_arr = search_file["BMR"]
    result_file = json.load(open("run/" + oper_dir+"/states/" + state_file))
    result_arr = ""
    for item in result_file["views"]:
        if("resource_id" in item and item["resource_id"] and item["resource_id"].split("/")[-1]==(search_arr)):
            try:
                result_arr = item["text"].replace("\n","").replace("\t","").replace("\r","")
            except:
                result_arr = None
    try:
        app_bmr = float(re.findall(r"[-+]?(?:\d*\.*\d+)",result_arr)[0])
    except:
        app_bmr = None
    try:
        subprocess.check_call(["adb","-s",device,"shell","pm clear",file])
    except:
        pass
    print(str(app_bmr))
    shutil.rmtree("run/" + oper_dir)
    os.makedirs("run/"+ oper_dir)
    return result + "||" + "BMR:" + str(app_bmr) + "]"

def goThroughItems(filelist,oper_dir,device):
    for file in filelist:
        outf = open("results/" + file,"w")
        for i in range(30):
            val = run(file,oper_dir,device,i)
            outf.write(val + "\n")
        

pq = mp.Queue()
if __name__ == "__main__":
    for item in available_devices:
        print(subprocess.check_output(["adb","-s",item,"root"]))
    chunks = np.array_split(whitelist,len(available_devices))
    devs = []
    for i in range(len(available_devices)):
        z = mp.Process(target=goThroughItems,args=(chunks[i],str(i),available_devices[i]))
        z.start()
        devs.append(z)
    for item in devs:
        item.join()
    pq.put(None)
    for dev in devs:
        dev.join()
    print("FINISHED",time.time()-start_tm)
