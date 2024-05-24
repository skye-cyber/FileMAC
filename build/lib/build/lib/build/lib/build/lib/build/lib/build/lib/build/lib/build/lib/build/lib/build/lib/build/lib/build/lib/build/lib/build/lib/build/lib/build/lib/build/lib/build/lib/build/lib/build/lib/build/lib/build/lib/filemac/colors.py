import os

from colorama import Fore, Style, init

init(autoreset=True)

if os.name == "posix":
    RESET = '\033[0m'

    RED = '\033[91m'
    DRED = '\033[1;91m'
    FRED = '\033[2;91m'

    GREEN = '\033[92m'
    DGREEN = '\033[1;92m'
    FGREEN = '\033[2;92m'

    YELLOW = '\033[93m'
    DYELLOW = '\033[1;93m'
    FYELLOW = '\033[2;93m'

    BLUE = '\033[94m'
    DBLUE = '\033[1;94m'
    FBLUE = '\033[2;94m'

    MAGENTA = '\033[95m'
    DMAGENTA = '\033[1;95m'
    FMAGENTA = '\033[2;95m'
    IMAGENTA = '\033[3;95m'

    CYAN = '\033[96m'
    DCYAN = '\033[1;96m'
    FCYAN = '\033[2;96m'
    ICYAN = '\033[3;96m'

    BWHITE = '\033[1m'
    BBWHITE = '\033[5;97;1m'

elif os.name == "nt":
    RESET = Style.RESET_ALL

    RED = Fore.LIGHTRED_EX
    DRED = Fore.RED
    FRED = Fore.RED

    GREEN = Fore.LIGHTGREEN_EX
    DGREEN = Fore.GREEN
    FGREEN = Fore.GREEN

    YELLOW = Fore.LIGHTYELLOW_EX
    FYELLOW = Fore.YELLOW
    DYELLOW = Fore.YELLOW

    BLUE = Fore.LIGHTBLUE_EX
    DBLUE = Fore.BLUE
    FBLUE = Fore.BLUE

    MAGENTA = Fore.LIGHTMAGENTA_EX
    DMAGENTA = Fore.MAGENTA
    IMAGENTA = Fore.LIGHTMAGENTA_EX
    FMAGENTA = Fore.MAGENTA

    CYAN = Fore.LIGHTCYAN_EX
    DCYAN = Fore.CYAN
    ICYAN = Fore.WHITE
    FCYAN = Fore.CYAN

    BWHITE = Fore.WHITE
    BWHITE = Fore.WHITE

# return RESET, RED, DRED, GREEN, DGREEN, YELLOW, DYELLOW, BLUE, DBLUE,
# MAGENTA, DMAGENTA, CYAN, DCYAN
