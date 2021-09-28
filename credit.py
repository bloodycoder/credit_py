import json
from commandHandler import *
def main():
    f = open("./credit.json", 'r')
    text = f.read()
    jsonObj = json.loads(text)
    f.close()
    comhan = CommandHandler(jsonObj) 
    comhan.prtJob(comhan.currentJobList, 0, NOLIMIT)
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

if __name__ == "__main__":
	main()