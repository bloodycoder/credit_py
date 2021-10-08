from logging import root
from os import rmdir
from beautiConsole import BeautiConsole
from log import CreditLog
import datetime
import functools
import json
from chinese_calendar import is_workday, is_holiday
from dropBox import dropBox
import threading
from queue import Queue
EXITCLIENT = 100
WEEKCARD = 12
WEEK = 7
NOLIMIT = -1
MONTH = 30
HALF_YEAR = 180
YEAR = 365
HOLIDAY_DISCOUNT = 6
FIRSTFREE_DISCOUNT = 4
def daysBetween(date1, date2):
    date1 = datetime.date(date1.year, date1.month, date1.day)
    return abs((date1-date2).days)

uploadThreadQueue = Queue()
class uploadThread(threading.Thread):
    def __init__(self, dropbox, comhand):
        threading.Thread.__init__(self)
        self.dropbox = dropbox
        self.comhand = comhand
    def run(self):
        self.dropbox.upload_file("./credit.json", "/credit.json")
        self.comhand.creditLog.uploadLog()
        uploadThreadQueue.get()
        uploadThreadQueue.task_done()
class FolderInfo():
    def __init__(self, folderJSON, folderName, cdIndex):
        self.folderJSON = folderJSON
        self.folderName = folderName
        self.cdIndex = cdIndex
class CommandHandler():
    def __init__(self, jobj):
        self.beauticonsole = BeautiConsole()
        self.jobj = jobj
        self.creditLog = CreditLog()
        self.credit = float(jobj.get("score"))
        self.rootJobList = jobj.get("jobList")
        self.currentJobList = self.rootJobList
        self.activities = jobj.get("activities")
        self.currentJobName = "全部任务"
        self.sortedJob = []
        self.dateNow = datetime.date.today()
        self.dropbox = dropBox()
        # this contains a pair (folderJson, folderName)
        self.folderInfoStack = []
        self.SortShopActivities()
    def isFirstFree(self):
        dateStr = self.jobj.get("lastBuyDate")
        if(dateStr == None):
            dateStr = '2021-09-20'
        dueDate = datetime.datetime.strptime(dateStr, '%Y-%m-%d')
        dateNow = datetime.date.today()
        daybetween = daysBetween(dueDate, dateNow)
        return daybetween>=1
    def SortShopActivities(self):
        def compare_activities(x,y):
            credit1 = int(x["name"].split('#')[1])
            credit2 = int(y["name"].split('#')[1])
            return credit1-credit2
        self.activities.sort(key=functools.cmp_to_key(compare_activities))
    def prtJob(self, jobRoot, cengji, daylimit):
        index = 0
        for job in jobRoot:
            jobName = job.get("jobName")
            credit = job.get("jobCredit")
            isStatic = job.get("static")
            if(isStatic != None and isStatic != 0):
                lastFinishDate = job.get("lastFinishDate")
                repeatTime = job.get("repeatTime")
                if(lastFinishDate != None and repeatTime!=None and repeatTime!=0):
                    lastFinishDate = datetime.datetime.strptime(lastFinishDate, '%Y-%m-%d')
                    daybetween = daysBetween(lastFinishDate, self.dateNow)
                    if(daybetween<repeatTime):
                        index+=1
                        continue
            if(daylimit == NOLIMIT):
                for i in range(0,cengji):
                    print("  ",end=''),
                if(cengji%2 == 0):
                    self.beauticonsole.colorPrint(str(index)+","+jobName+"#"+str(credit),BeautiConsole.RED, -1)
                else:
                    self.beauticonsole.colorPrint(str(index)+","+jobName+"#"+str(credit),BeautiConsole.BLUE, -1)
            else:
                dateStr = job.get("dueDate")
                dueDate = datetime.datetime.strptime(dateStr, '%Y-%m-%d')
                dateNow = datetime.date.today()
                daybetween = daysBetween(dueDate, dateNow)
                # i dont think this is useful

                print(daybetween)
            subJob = job.get("subJob")
            if(subJob != None and len(subJob)>0):
                self.prtJob(subJob, cengji+1, daylimit)
            index+=1
    
    def saveJson(self):
        self.jobj['score'] = self.credit
        self.jobj['save_version'] = self.jobj['save_version']+1
        jsonStr = json.dumps(self.jobj, ensure_ascii=False)
        f = open("credit.json",'w')
        f.write(jsonStr)
        f.close()
        mythread = uploadThread(self.dropbox, self, )
        uploadThreadQueue.put(mythread)
        mythread.start()

    def parseStr(self, cmd):
        errcode = 0
        s = cmd.split(" ")
        if(len(s)>0):
            if(s[0] == 'quit' or s[0] == 'exit' or s[0] == 'q' or s[0] == 'e'):
                self.saveJson()
                uploadThreadQueue.join()
                return EXITCLIENT
            elif(s[0] == 'log'):
                if(len(s)>1):
                    self.creditLog.showLog(True)
                else:
                    self.creditLog.showLog(False)
            elif(s[0] == 'help'):
                print("shop[-t | -r]:显示全部\nbuy:购买\nfinish:完成任务")
                print("touch[-l(-list)| -r(root)][-s(static)]")
                print("log[-p]")
                print('exit:离开')
            elif(s[0] == 'ls' or s[0] == 'l' or s[0] == 'll'):
                self.beauticonsole.colorPrint(self.currentJobName,BeautiConsole.YELLOW,-1)
                if(len(self.currentJobList)>0):
                    self.prtJob(self.currentJobList, 0, NOLIMIT)
                else:
                    print("暂时无任务\n")
            elif(s[0] == 'cd'):
                if(len(s)>1 and s[1] == '~'):
                    self.currentJobList = self.jobj.get('jobList')
                    self.currentJobName = '全部任务'
                    self.folderInfoStack = []
                    return 0
                elif(len(s)>1 and s[1] == '..'):
                    if(len(self.folderInfoStack) == 0):
                        return 0
                    tmpInfo = self.folderInfoStack[-1]
                    self.folderInfoStack = self.folderInfoStack[:len(self.folderInfoStack)-1]
                    self.currentJobList = tmpInfo.folderJSON
                    self.currentJobName = tmpInfo.folderName
                    return 0
                index = int(s[1])
                if(index<len(self.currentJobList)):
                    # can cd 1
                    job = self.currentJobList[index]
                    tmpInfo = FolderInfo(self.currentJobList, self.currentJobName, index)
                    self.folderInfoStack.append(tmpInfo)
                    self.currentJobIndex = index
                    self.currentJobName = job.get("jobName")
                    self.currentJobList = job.get('subJob')
                    return 0
                print("切换目录错误\n")
            elif(s[0] == 'touch' or s[0] == 't'):
                if(len(s)>=2 and (s[1] == 'list' or s[1]=="l")):
                    print("公共部分?")
                    commonPart = input()
                    jobdate = "2099-12-29"
                    print("从哪到哪? num-num")
                    fromToStr = input().split("-")
                    fromNum = int(fromToStr[0])
                    toNum = int(fromToStr[1])
                    if(fromNum > toNum):
                        return 0
                    print("credit? a number")
                    fenshu = input()
                    if(len(fenshu) == 0):
                        fenshu = 0
                    for i in range(fromNum, toNum+1):
                        self.currentJobList.append(getJobDict(commonPart+"_"+str(i), int(fenshu), jobdate, []))
                    self.saveJson()
                    return 0
                rootFlag = False
                staticFlag = False # 静态工作
                if(len(s)>=2 and s[1] == 'r'):
                    rootFlag = True
                if(len(s)>=2 and s[1] == 's'):
                    staticFlag = True
                print("jobname?")
                jobname = input()
                if(len(jobname) == 0):
                    print("任务名不能为空")
                    return 0
                print("jobdate?yyyy-mm-dd or mm-dd")
                jobdate = input()
                if(len(jobdate)<=5):
                    jobdate = '2099-12-29'
                print("credit?")
                credit = input()
                if(len(credit) == 0):
                    credit = 0
                newJob = getJobDict(jobname, int(credit), jobdate, [])
                if(staticFlag == True):
                    newJob["static"] = 1
                    print("repleat time?int")
                    repeatTime = int(input())
                    newJob["repeatTime"] = repeatTime
                if(rootFlag):
                    self.rootJobList.append(newJob)
                else:
                    self.currentJobList.append(newJob)
                self.saveJson()
            elif(s[0] == 'finish' or s[0] == 'f'):
                if((len(s)>=2 and s[1] == 'c') or len(s) == 1):
                    if(len(self.folderInfoStack) == 0):
                        self.beauticonsole.colorPrint("错误，不能在根目录完成全部任务", BeautiConsole.RED, -1)
                        return 0
                    print('你确定要完成任务',end='')
                    self.beauticonsole.colorPrint(self.currentJobName, BeautiConsole.YELLOW, -1)
                    yStr = input()
                    if(yStr == 'y'):
                        tmpInfo = self.folderInfoStack[-1]
                        #self.folderInfoStack = self.folderInfoStack[:len(self.folderInfoStack)-1]
                        self.currentJobList = tmpInfo.folderJSON
                        self.currentJobName = tmpInfo.folderName
                        index = tmpInfo.cdIndex
                        job = self.currentJobList[index]
                        self.credit += job.get('jobCredit')
                        self.currentJobList.pop(index)
                        self.creditLog.info("完成任务"+job.get('jobName')+"获得分值"+str(job.get('jobCredit'))+",现有分值"+str(self.credit))
                        if(len(self.currentJobList)>index):
                            job = self.currentJobList[index]
                            self.currentJobIndex = index
                            self.currentJobName = job.get("jobName")
                            self.currentJobList = job.get('subJob')
                        else:
                            self.folderInfoStack = self.folderInfoStack[:len(self.folderInfoStack)-1]
                        print('成功')
                else:
                    index = int(s[1])
                    if(index>=len(self.currentJobList)):
                        self.beauticonsole.colorPrint("error", BeautiConsole.RED, -1)
                    job = self.currentJobList[index]
                    print('你确定要完成任务',end='')
                    self.beauticonsole.colorPrint(job['jobName'], BeautiConsole.YELLOW, -1)
                    yStr = input()
                    if(yStr == 'y'):
                        self.credit += job.get("jobCredit")
                        self.beauticonsole.colorPrint("成功", BeautiConsole.RED, -1)
                        self.creditLog.info("完成任务"+job.get('jobName')+"获得分值"+str(job.get('jobCredit'))+",现有分值"+str(self.credit))
                        if(job.get("static") == None or job.get("static") == 0):
                            self.currentJobList.pop(index)
                        else:
                            job["lastFinishDate"] = str(self.dateNow.year)+"-"+str(self.dateNow.month)+"-"+str(self.dateNow.day)
                    else:
                        return 0
                self.saveJson()
            elif (s[0] == 'remove' or s[0] == 'rm'):
                index = int(s[1])
                job = self.currentJobList[index]
                print('你确定要删除任务',end='')
                self.beauticonsole.colorPrint(job.get("jobName"),BeautiConsole.YELLOW,-1)
                yStr = input()
                if(yStr == 'y'):
                    self.currentJobList.pop(index)
                    self.creditLog.info("删除任务"+job.get('jobName')+",现有分值"+str(self.credit))
                    print("成功")
            elif (s[0] == 'shop' or s[0] == 's'):
                if(len(s)>=2 and (s[1] == 'touch' or s[1] == 't')):
                    print("新的活动名称?")
                    acname = input()
                    if(len(acname) == 0):
                        print("活动名不能为空")
                        return 0
                    print("credit")
                    credit = input()
                    if(len(credit) == 0):
                        credit = "0"
                    newActivity ={}
                    newActivity["name"] = acname + "#" + credit
                    self.activities.append(newActivity)
                    self.creditLog.info("新增活动"+acname+",价格"+str(credit)+",现有分值"+str(self.credit))
                    self.SortShopActivities()
                elif(len(s)>=3 and s[1] == 'rm'):
                    index = int(s[2])
                    if(len(self.activities)>index):
                        print("你确定要删除活动",end='')
                        activityDel = self.activities[index]["name"]
                        self.beauticonsole.colorPrint(activityDel,BeautiConsole.YELLOW,-1)
                        yStr = input()
                        if(yStr == 'y'):
                            self.activities.pop(index)
                            print("成功")
                            self.creditLog.info("删除活动"+activityDel+",现有分值"+str(self.credit))
                else:
                    zhoukacnt = self.jobj.get("weekCard")
                    print("欢迎来到超市，显示所有娱乐活动:\n现有分值",end="")
                    self.beauticonsole.colorPrint(str(self.credit),BeautiConsole.YELLOW,-1)
                    print("周卡张数",end="")
                    self.beauticonsole.colorPrint(str(zhoukacnt),BeautiConsole.YELLOW,-1)
                    if(is_holiday(self.dateNow)):
                        print("今天是活动日, 所有商品打"+str(HOLIDAY_DISCOUNT)+"折")
                    if(self.isFirstFree()):
                        self.beauticonsole.colorPrint("首次免费生效",BeautiConsole.RED, -1)
                    for i in range (0, len(self.activities)):
                        name = self.activities[i]["name"]
                        if(i%2 == 0):
                            self.beauticonsole.colorPrint(str(i)+","+name,BeautiConsole.PURPLE,-1)
                        else:
                            self.beauticonsole.colorPrint(str(i)+","+name,BeautiConsole.YELLOW,-1)
            elif((s[0] == 'buy' or s[0] == 'b') and len(s)>=2):
                index = int(s[1])
                if(index>=len(self.activities)):
                    print('err')
                    return 0
                name = self.activities[index]["name"]
                activity = name.split("#")
                creditNeed = float(activity[1])
                if(is_holiday(self.dateNow)):
                    creditNeed = creditNeed*(float(HOLIDAY_DISCOUNT)/10)
                if(self.isFirstFree()):
                    creditNeed = creditNeed*(float(FIRSTFREE_DISCOUNT)/10)
                print("确定要花"+str(creditNeed)+"来兑换"+activity[0]+"吗？(Y/N)")
                line = input()
                if(line == 'y' or line == 'Y'):
                    self.credit -= creditNeed
                    if(activity[0] == '周卡购买'):
                        weekCard = self.jobj.get("weekCard")
                        if(weekCard == None):
                            weekCard = 0
                        weekCard+=1
                        self.jobj["weekCard"] = weekCard
                    self.jobj["lastBuyDate"] = str(self.dateNow.year)+'-'+str(self.dateNow.month)+'-'+str(self.dateNow.day)
                    print("成功")
                self.saveJson()
                self.creditLog.info("购买活动"+name+",现有分值"+str(self.credit))
            return errcode

def getJobDict(jobName, jobCredit, dueDate, subJob):
    newJob = {}
    newJob["jobName"] = jobName
    newJob["jobCredit"] = jobCredit
    newJob["dueDate"] = dueDate
    newJob["subJob"] = subJob
    return newJob