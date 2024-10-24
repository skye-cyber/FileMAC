import os

from colorama import Fore, Style, init

init(autoreset=True)

if os.name == "posix":
    RESET = '\033[0m'  # Reset to default text color

    # Red Variants
    RED = '\033[91m'  # Normal RED
    DRED = '\033[1;91m'  # Deep RED
    FRED = '\033[2;91m'  # Faint red
    IRED = '\033[3;91m'  # Indented RED
    LRED = '\033[4;91m'  # Underlined RED
    URED = '\033[5;91m'  # Blinking RED

    # Green Variants
    GREEN = '\033[92m'  # Normal green
    DGREEN = '\033[1;92m'  # Deep green
    FGREEN = '\033[2;92m'  # Faint green
    IGREEN = '\033[3;92m'  # Indented GREEN
    LGREEN = '\033[4;92m'  # Underlined GREEN
    UGREEN = '\033[5;92m'  # Blinking GREEN

    # Yellow Variants
    YELLOW = '\033[93m'  # Normal yellow
    DYELLOW = '\033[1;93m'  # Deep YELLOW
    FYELLOW = '\033[2;93m'  # Faint YELLOW
    IYELLOW = '\033[3;93m'  # Indented YELLOW
    LYELLOW = '\033[4;93m'  # Underlined YELLOW
    UYELLOW = '\033[5;93m'  # Blinking YELLOW

    # Blue Variants
    BLUE = '\033[94m'  # Normal BLUE
    DBLUE = '\033[1;94m'  # Deep BLUE
    FBLUE = '\033[2;94m'  # Faint Blue
    IBLUE = '\033[3;94m'  # Indented BLUE
    LBLUE = '\033[4;94m'  # Underlined BLUE
    UBLUE = '\033[5;94m'  # Blinking BLUE

    # Magenta Variants
    MAGENTA = '\033[95m'  # Normal MAGENTA
    DMAGENTA = '\033[1;95m'  # Deep MAGENTA
    FMAGENTA = '\033[2;95m'  # Faint MAGENTA
    IMAGENTA = '\033[3;95m'  # Indented MAGENTA
    LMAGENTA = '\033[4;95m'  # Underlined MAGENTA
    UMAGENTA = '\033[5;95m'  # Blinking MAGENTA

    # Cyan Variants
    CYAN = '\033[96m'  # Normal cyan
    DCYAN = '\033[1;96m'  # Deep CYAN
    FCYAN = '\033[2;96m'  # Faint cyan
    ICYAN = '\033[3;96m'  # Indented CYAN
    LCYAN = '\033[4;96m'  # Underlined CYAN
    UCYAN = '\033[5;96m'  # Blinking CYAN

    # White Variants
    BWHITE = '\033[1m'  # Bold white
    BBWHITE = '\033[5;97;1m'  # Bold Blinking white
    WHITE = '\033[97m'  # Normal white
    DWHITE = '\033[1;97m'  # Deep white
    FWHITE = '\033[2;97m'  # Faint white
    IWHITE = '\033[3;97m'  # Indented white
    LWHITE = '\033[4;97m'  # Underlined white
    UWHITE = '\033[5;97m'  # Blinking white


if os.name == "nt":
    RESET = Style.RESET_ALL

    # Red Variants
    RED = Fore.LIGHTRED_EX
    DRED = Fore.RED
    FRED = Fore.RED
    IRED = Fore.RED
    LRED = Fore.LIGHTRED_EX  # Underlined RED
    URED = Fore.RED  # Blinking not directly supported, using RED

    # Green Variants
    GREEN = Fore.LIGHTGREEN_EX
    DGREEN = Fore.GREEN
    FGREEN = Fore.GREEN
    IGREEN = Fore.GREEN
    LGREEN = Fore.LIGHTGREEN_EX  # Underlined GREEN
    UGREEN = Fore.GREEN  # Blinking not directly supported, using GREEN

    # Yellow Variants
    YELLOW = Fore.LIGHTYELLOW_EX
    DYELLOW = Fore.YELLOW
    FYELLOW = Fore.YELLOW
    IYELLOW = Fore.YELLOW
    LYELLOW = Fore.LIGHTYELLOW_EX  # Underlined YELLOW
    UYELLOW = Fore.YELLOW  # Blinking not directly supported, using YELLOW

    # Blue Variants
    BLUE = Fore.LIGHTBLUE_EX
    DBLUE = Fore.BLUE
    FBLUE = Fore.BLUE
    IBLUE = Fore.BLUE
    LBLUE = Fore.LIGHTBLUE_EX  # Underlined BLUE
    UBLUE = Fore.BLUE  # Blinking not directly supported, using BLUE

    # Magenta Variants
    MAGENTA = Fore.LIGHTMAGENTA_EX
    DMAGENTA = Fore.MAGENTA
    FMAGENTA = Fore.MAGENTA
    IMAGENTA = Fore.LIGHTMAGENTA_EX
    LMAGENTA = Fore.LIGHTMAGENTA_EX  # Underlined MAGENTA
    UMAGENTA = Fore.MAGENTA  # Blinking not directly supported, using MAGENTA

    # Cyan Variants
    CYAN = Fore.LIGHTCYAN_EX
    DCYAN = Fore.CYAN
    ICYAN = Fore.WHITE  # Indented CYAN
    FCYAN = Fore.CYAN
    LCYAN = Fore.LIGHTCYAN_EX  # Underlined CYAN
    UCYAN = Fore.CYAN  # Blinking not directly supported, using CYAN

    # White Variants
    BWHITE = Fore.WHITE
    BBWHITE = Fore.WHITE  # Blinking not directly supported, using WHITE
    WHITE = Fore.WHITE
    DWHITE = Fore.WHITE  # Deep white (not distinct in colorama)
    FWHITE = Fore.WHITE  # Faint white (not distinct in colorama)
    IWHITE = Fore.WHITE  # Indented white (not distinct in colorama)
    LWHITE = Fore.WHITE  # Underlined white (not distinct in colorama)
    UWHITE = Fore.WHITE  # Blinking not directly supported, using WHITE
