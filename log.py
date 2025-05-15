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
        self.dropbox.download_files("/"+self.curLogFile,"./log/"+self.curLogFile)
        #logging.basicConfig(level=logging.INFO, filename=self.curLogFile,format="%(levelname)s:%(asctime)s:%(message)s\n")

        fh = logging.FileHandler("./log/"+self.curLogFile, mode = 'a', encoding='UTF-8', delay=False)
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
        self.logger = logging.getLogger()
        self.logger.addHandler(fh)
        self.logger.setLevel(logging.INFO)
    def showLog(self, showPrev):
        if(showPrev):
            try:
                f = open(self.prevLogFile, 'r', encoding='UTF-8')
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
        f = open('./log/'+self.curLogFile, 'r', encoding='UTF-8')
        text = f.readlines()
        if(len(text)<100):
            for i in range(len(text)):
                print(text[i])
        else:
            for i in range(len(text)-100,len(text)):
                print(text[i])
        f.close()
    def info(self, msg):
        self.logger.info(msg)
    def uploadLog(self):
        self.dropbox.upload_file("./log/"+self.curLogFile,"/"+self.curLogFile)
