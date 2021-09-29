import colorama
from colorama import init
init(autoreset=True)
class BeautiConsole():
    WHITE = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE  = 4
    PURPLE = 5
    LOWBLUE = 6
    GREY = 7
    def colorPrint(self, words, fontColor, bgColor):
        fontColor += 30
        if(bgColor == -1):
            print("\033["+str(fontColor)+";4m"+words+"\033[0m")
        else:
            bgColor +=40
            print("\033["+str(bgColor)+";"+str(fontColor)+";4m"+words+"\033[0m")
