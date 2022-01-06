import colorama
import sys
from colorama import init
init(autoreset=True)
class BeautiConsole():
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE  = 4
    PURPLE = 5
    LOWBLUE = 6
    WHITE = 7
    GREY = 8
    # set terminal color
    def console (self, color):
        if sys.platform[:3] == 'win':
            import ctypes
            kernel32 = ctypes.windll.LoadLibrary('kernel32.dll')
            GetStdHandle = kernel32.GetStdHandle
            SetConsoleTextAttribute = kernel32.SetConsoleTextAttribute
            GetStdHandle.argtypes = [ ctypes.c_uint32 ]
            GetStdHandle.restype = ctypes.c_size_t
            SetConsoleTextAttribute.argtypes = [ ctypes.c_size_t, ctypes.c_uint16 ]
            SetConsoleTextAttribute.restype = ctypes.c_long
            handle = GetStdHandle(0xfffffff5)
            if color < 0: color = 7
            result = 0
            if (color & 1): result |= 4
            if (color & 2): result |= 2
            if (color & 4): result |= 1
            if (color & 8): result |= 8
            if (color & 16): result |= 64
            if (color & 32): result |= 32
            if (color & 64): result |= 16
            if (color & 128): result |= 128
            SetConsoleTextAttribute(handle, result)
        else:
            if color >= 0:
                foreground = color & 7
                background = (color >> 4) & 7
                bold = color & 8
                sys.stdout.write("\033[%s3%d;4%dm"%(bold and "01;" or "", foreground, background))
                sys.stdout.flush()
            else:
                sys.stdout.write("\033[0m")
                sys.stdout.flush()
        return 0
        
    def echo (self, color, text):
        self.console(color)
        sys.stdout.write(text)
        sys.stdout.write('\n')
        sys.stdout.flush()
        return 0

    def colorPrint(self, words, fontColor, bgColor):
        """
        deprecated
        fontColor += 30
        if(bgColor == -1):
            print("\033["+str(fontColor)+";4m"+words+"\033[0m")
        else:
            bgColor +=40
            print("\033["+str(bgColor)+";"+str(fontColor)+";4m"+words+"\033[0m")
        """
        if sys.platform[:3] == 'win':
            self.echo(fontColor, words)
        else:
            print("\033["+str(fontColor)+";4m"+words+"\033[0m")

if __name__ == "__main__":
    mysb = BeautiConsole() 
    for i in range(0,100):
        mysb.echo(i,str(i))