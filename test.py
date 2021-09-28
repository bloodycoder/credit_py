import requests
def main():

    testwrite()
    #testweb()
def getHTMLText(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"

def testwrite():
    jsonStr = '{"score": 10, "jobList": [{"jobName": "eat dinner", "jobCredit": 1, "subJob": [], "dueDate": "2021-09-30"}], "activities": ["增加活动#2", "喝酒半杯#5", "绣湖游戏#10", "周卡购买#10"]}'
    f = open("credit.json",'w')
    f.write(jsonStr)
    f.close()

def testweb():
    print('begin testweb')
    url ="http://www.baidu.com"
    print(getHTMLText(url))

if __name__ == "__main__":
	main()