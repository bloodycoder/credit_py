import unittest
import json
from beautiConsole import *
from commandHandler import *
from log import CreditLog
class Test(unittest.TestCase):
    def test_init(self):
        print('begin test')
    def test_console(self):
        console = BeautiConsole()
        console.colorPrint("hello", console.GREEN, console.GREY)
    def test_json(self):
        pass
        f = open("./credit.json", 'r')
        text = f.read()
        jsonObj = json.loads(text)
        f.close()
        comhan = CommandHandler(jsonObj) 
        comhan.prtJob(comhan.currentJobList, 0, NOLIMIT)
        comhan.parseStr("cd 0")
        comhan.prtJob(comhan.currentJobList, 0, NOLIMIT)
        comhan.parseStr("cd 1")
        comhan.parseStr("s t")
    def test_log(self):
        creditlog = CreditLog()
if __name__ == '__main__':
    unittest.main()