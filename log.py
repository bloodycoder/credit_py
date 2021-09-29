import datetime
import logging
import dropBox
class CreditLog():
    def __init__(self) -> None:
        self.dateNow = datetime.date.today()
        self.currentDateStr = str(self.dateNow.year)+'_'+str(self.dateNow.month) 
        curMonth = self.dateNow.month
        if(curMonth == 1):
            self.prevDateStr = str(self.dateNow.year-1)+'_'+str(12)
        else:
            self.prevDateStr = str(self.dateNow.year)+'_'+str(self.dateNow.month-1)
        self.curLogFile = 'credit'+self.currentDateStr+'.log'
        self.prevLogFile = 'credit'+self.prevDateStr+'.log'
        self.dropbox = dropBox.dropBox()
        self.dropbox.download_files("/"+self.curLogFile,"./"+self.curLogFile)
        logging.basicConfig(level=logging.INFO, filename=self.curLogFile,format="%(levelname)s:%(asctime)s:%(message)s")
    def showLog(self, showPrev):
        if(showPrev):
            try:
                f = open(self.prevLogFile, 'r')
                text = f.readlines()
                if(len(text)<100):
                    for i in range(len(text)):
                        print(text[i])
                else:
                    for i in range(len(text)-100,len(text)):
                        print(text[i])
                f.close()
            except FileNotFoundError:
                print("file not found")
        f = open(self.curLogFile, 'r')
        text = f.readlines()
        if(len(text)<100):
            for i in range(len(text)):
                print(text[i])
        else:
            for i in range(len(text)-100,len(text)):
                print(text[i])
        f.close()
    def info(self, msg):
        logging.info(msg)
    def uploadLog(self):
        self.dropbox.upload_file("./"+self.curLogFile,"/"+self.curLogFile)