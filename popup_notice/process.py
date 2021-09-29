import subprocess
import time
import sched
windowsLink = "D:\github-code\credit_py\popup_notice\popup.bat"
timeToSleep = 2400
def doprocessWindowsPopUp():
    # for windows version
    p = subprocess.Popen("cmd.exe /c" + windowsLink, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
def macVersion():
    # for mac
    pass
if __name__ == '__main__':
    while(True):
        print("begin new loop")
        curTime = time.time()
        goalTime = curTime+timeToSleep
        while(True):
            time.sleep(3)
            if(time.time()>goalTime):
                print("timeGap="+str(time.time()-curTime))
                break
        doprocessWindowsPopUp()