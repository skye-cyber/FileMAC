import os

from colorama import Fore, Style, init

init(autoreset=True)

if os.name == "posix":
    RESET = '\033[0m'
    RED = '\033[91m'
    DRED = '\033[1;91m'
    GREEN = '\033[92m'
    DGREEN = '\033[1;92m'
    YELLOW = '\033[93m'
    DYELLOW = '\033[1;93m'
    BLUE = '\033[94m'
    DBLUE = '\033[1;94m'
    MAGENTA = '\033[95m'
    DMAGENTA = '\033[1;95m'
    CYAN = '\033[96m'
    DCYAN = '\033[1;96m'

elif os.name == "nt":
    RESET = Style.RESET_ALL
    RED = Fore.LIGHTRED_EX
    DRED = Fore.RED
    GREEN = Fore.LIGHTGREEN_EX
    DGREEN = Fore.GREEN
    YELLOW = Fore.LIGHTYELLOW_EX
    DYELLOW = Fore.YELLOW
    BLUE = Fore.LIGHTBLUE_EX
    DBLUE = Fore.BLUE
    MAGENTA = Fore.LIGHTMAGENTA_EX
    DMAGENTA = Fore.MAGENTA
    CYAN = Fore.LIGHTCYAN_EX
    DCYAN = Fore.CYAN

#return RESET, RED, DRED, GREEN, DGREEN, YELLOW, DYELLOW, BLUE, DBLUE,
#MAGENTA, DMAGENTA, CYAN, DCYAN
