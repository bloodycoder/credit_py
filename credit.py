import json
from commandHandler import *
from dropBox import dropBox
def main():
    jsonObj = initCredit()
    comhan = CommandHandler(jsonObj) 
    comhan.prtJob(comhan.currentJobList, 0, NOLIMIT,'')
    while(True):
        print('picard>',end="")
        cmd = input().lower()
        err = comhan.parseStr(cmd)
        if(err == -1):
            print("Server error please retry.")
            break
        elif(err == EXITCLIENT):
            print('Exit system.')
            break

def initCredit():
    mydrop = dropBox()
    mydrop.download_files("/credit.json","./credit_dropbox.json")
    f = open("./credit_dropbox.json", 'r')
    text = f.read()
    jsonObjDrop = json.loads(text)
    f.close()
    if(jsonObjDrop.get("save_version") == None):
        jsonObjDrop["save_version"] = 0
    f = open("./credit.json", 'r')
    text = f.read()
    jsonObjLocal = json.loads(text)
    f.close()
    if(jsonObjLocal.get("save_version") == None):
        jsonObjLocal["save_version"] = 1
    if(jsonObjLocal["save_version"]<jsonObjDrop["save_version"]):
        print("use online version")
        return jsonObjDrop
    else:
        print("use local version")
        return jsonObjLocal
if __name__ == "__main__":
	main()