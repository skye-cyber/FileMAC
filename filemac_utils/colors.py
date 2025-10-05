import os

from colorama import Fore, Style, init

init(autoreset=True)


class foreground:
    if os.name == "posix":
        RESET = "\033[0m"  # Reset to default text color

        # Red Variants
        RED_FG = "\033[91m"  # Normal RED
        BRED_FG = "\033[1;91m"  # Deep RED
        FRED_FG = "\033[2;91m"  # Faint red
        IRED_FG = "\033[3;91m"  # Indented RED
        LRED_FG = "\033[4;91m"  # Underlined RED
        URED_FG = "\033[5;91m"  # Blinking RED

        # Green Variants
        GREEN_FG = "\033[92m"  # Normal green
        BGREEN_FG = "\033[1;92m"  # Deep green
        FGREEN_FG = "\033[2;92m"  # Faint green
        IGREEN_FG = "\033[3;92m"  # Indented GREEN
        LGREEN_FG = "\033[4;92m"  # Underlined GREEN
        UGREEN_FG = "\033[5;92m"  # Blinking GREEN

        # Yellow Variants
        YELLOW_FG = "\033[93m"  # Normal yellow
        BYELLOW_FG = "\033[1;93m"  # Deep YELLOW
        FYELLOW_FG = "\033[2;93m"  # Faint YELLOW
        IYELLOW_FG = "\033[3;93m"  # Indented YELLOW
        LYELLOW_FG = "\033[4;93m"  # Underlined YELLOW
        UYELLOW_FG = "\033[5;93m"  # Blinking YELLOW

        # Blue Variants
        BLUE_FG = "\033[94m"  # Normal BLUE
        BBLUE_FG = "\033[1;94m"  # Deep BLUE
        FBLUE_FG = "\033[2;94m"  # Faint Blue
        IBLUE_FG = "\033[3;94m"  # Indented BLUE
        LBLUE_FG = "\033[4;94m"  # Underlined BLUE
        UBLUE_FG = "\033[5;94m"  # Blinking BLUE

        # Magenta Variants
        MAGENTA_FG = "\033[95m"  # Normal MAGENTA
        BMAGENTA_FG = "\033[1;95m"  # Deep MAGENTA
        FMAGENTA_FG = "\033[2;95m"  # Faint MAGENTA
        IMAGENTA_FG = "\033[3;95m"  # Indented MAGENTA
        LMAGENTA_FG = "\033[4;95m"  # Underlined MAGENTA
        UMAGENTA_FG = "\033[5;95m"  # Blinking MAGENTA

        # Cyan Variants
        CYAN_FG = "\033[96m"  # Normal cyan
        DCYAN_FG = "\033[1;96m"  # Deep CYAN
        FCYAN_FG = "\033[2;96m"  # Faint cyan
        ICYAN_FG = "\033[3;96m"  # Indented CYAN
        LCYAN_FG = "\033[4;96m"  # Underlined CYAN
        UCYAN_FG = "\033[5;96m"  # Blinking CYAN

        # White Variants
        BWHITE_FG = "\033[1m"  # Bold white
        BBWHITE_FG = "\033[5;97;1m"  # Bold Blinking white
        WHITE_FG = "\033[97m"  # Normal white
        DWHITE_FG = "\033[1;97m"  # Deep white
        FWHITE_FG = "\033[2;97m"  # Faint white
        IWHITE_FG = "\033[3;97m"  # Indented white
        LWHITE_FG = "\033[4;97m"  # Underlined white
        UWHITE_FG = "\033[5;97m"  # Blinking white

    if os.name == "nt":
        RESET = Style.RESET_ALL

        # Red Variants
        RED_FG = Fore.LIGHTRED_EX
        BRED_FG = Fore.RED
        FRED_FG = Fore.RED
        IRED_FG = Fore.RED
        LRED_FG = Fore.LIGHTRED_EX  # Underlined RED
        URED_FG = Fore.RED  # Blinking not directly supported, using RED

        # Green Variants
        GREEN_FG = Fore.LIGHTGREEN_EX
        BGREEN_FG = Fore.GREEN
        FGREEN_FG = Fore.GREEN
        IGREEN_FG = Fore.GREEN
        LGREEN_FG = Fore.LIGHTGREEN_EX  # Underlined GREEN
        UGREEN_FG = Fore.GREEN  # Blinking not directly supported, using GREEN

        # Yellow Variants
        YELLOW_FG = Fore.LIGHTYELLOW_EX
        BYELLOW_FG = Fore.YELLOW
        FYELLOW_FG = Fore.YELLOW
        IYELLOW_FG = Fore.YELLOW
        LYELLOW_FG = Fore.LIGHTYELLOW_EX  # Underlined YELLOW
        UYELLOW_FG = Fore.YELLOW  # Blinking not directly supported, using YELLOW

        # Blue Variants
        BLUE_FG = Fore.LIGHTBLUE_EX
        BBLUE_FG = Fore.BLUE
        FBLUE_FG = Fore.BLUE
        IBLUE_FG = Fore.BLUE
        LBLUE_FG = Fore.LIGHTBLUE_EX  # Underlined BLUE
        UBLUE_FG = Fore.BLUE  # Blinking not directly supported, using BLUE

        # Magenta Variants
        MAGENTA_FG = Fore.LIGHTMAGENTA_EX
        BMAGENTA_FG = Fore.MAGENTA
        FMAGENTA_FG = Fore.MAGENTA
        IMAGENTA_FG = Fore.LIGHTMAGENTA_EX
        LMAGENTA_FG = Fore.LIGHTMAGENTA_EX  # Underlined MAGENTA
        UMAGENTA_FG = Fore.MAGENTA  # Blinking not directly supported, using MAGENTA

        # Cyan Variants
        CYAN_FG = Fore.LIGHTCYAN_EX
        DCYAN_FG = Fore.CYAN
        ICYAN_FG = Fore.WHITE  # Indented CYAN
        FCYAN_FG = Fore.CYAN
        LCYAN_FG = Fore.LIGHTCYAN_EX  # Underlined CYAN
        UCYAN_FG = Fore.CYAN  # Blinking not directly supported, using CYAN

        # White Variants
        BWHITE_FG = Fore.WHITE
        BBWHITE_FG = Fore.WHITE  # Blinking not directly supported, using WHITE
        WHITE_FG = Fore.WHITE
        DWHITE_FG = Fore.WHITE  # Deep white (not distinct in colorama)
        FWHITE_FG = Fore.WHITE  # Faint white (not distinct in colorama)
        IWHITE_FG = Fore.WHITE  # Indented white (not distinct in colorama)
        LWHITE_FG = Fore.WHITE  # Underlined white (not distinct in colorama)
        UWHITE_FG = Fore.WHITE  # Blinking not directly supported, using WHITE


class background:
    if os.name == "posix":
        RESET = "\033[0m"  # Reset to default text color

        # Red Variants
        RED_BG = "\033[91m"  # Normal RED
        BRED_BG = "\033[1;41m"  # Deep RED
        FRED_BG = "\033[2;41m"  # Faint red
        IRED_BG = "\033[3;41m"  # Indented RED
        LRED_BG = "\033[4;41m"  # Underlined RED
        URED_BG = "\033[5;41m"  # Blinking RED

        # Green Variants
        GREEN_BG = "\033[42m"  # Normal green
        BGREEN_BG = "\033[1;42m"  # Deep green
        FGREEN_BG = "\033[2;42m"  # Faint green
        IGREEN_BG = "\033[3;42m"  # Indented GREEN
        LGREEN_BG = "\033[4;42m"  # Underlined GREEN
        UGREEN_BG = "\033[5;42m"  # Blinking GREEN

        # Yellow Variants
        YELLOW_BG = "\033[43m"  # Normal yellow
        BYELLOW_BG = "\033[1;43m"  # Deep YELLOW
        FYELLOW_BG = "\033[2;43m"  # Faint YELLOW
        IYELLOW_BG = "\033[3;43m"  # Indented YELLOW
        LYELLOW_BG = "\033[4;43m"  # Underlined YELLOW
        UYELLOW_BG = "\033[5;43m"  # Blinking YELLOW

        # Blue Variants
        BLUE_BG = "\033[44m"  # Normal BLUE
        BBLUE_BG = "\033[1;44m"  # Deep BLUE
        FBLUE_BG = "\033[2;44m"  # Faint Blue
        IBLUE_BG = "\033[3;44m"  # Indented BLUE
        LBLUE_BG = "\033[4;44m"  # Underlined BLUE
        UBLUE_BG = "\033[5;44m"  # Blinking BLUE

        # Magenta Variants
        MAGENTA_BG = "\033[45m"  # Normal MAGENTA
        BMAGENTA_BG = "\033[1;45m"  # Deep MAGENTA
        FMAGENTA_BG = "\033[2;45m"  # Faint MAGENTA
        IMAGENTA_BG = "\033[3;45m"  # Indented MAGENTA
        LMAGENTA_BG = "\033[4;45m"  # Underlined MAGENTA
        UMAGENTA_BG = "\033[5;45m"  # Blinking MAGENTA_BG

        # Cyan Variants
        CYAN_BG = "\033[46m"  # Normal cyan
        DCYAN_BG = "\033[1;46m"  # Deep CYAN
        FCYAN_BG = "\033[2;46m"  # Faint cyan
        ICYAN_BG = "\033[3;46m"  # Indented CYAN
        LCYAN_BG = "\033[4;46m"  # Underlined CYAN
        UCYAN_BG = "\033[5;46m"  # Blinking CYAN

        # White Variants
        BWHITE_BG = "\033[1m"  # Bold white
        BBWHITE_BG = "\033[5;47;1m"  # Bold Blinking white
        WHITE_BG = "\033[47m"  # Normal white
        DWHITE_BG = "\033[1;47m"  # Deep white
        FWHITE_BG = "\033[2;47m"  # Faint white
        IWHITE_BG = "\033[3;47m"  # Indented white
        LWHITE_BG = "\033[4;47m"  # Underlined white
        UWHITE_BG = "\033[5;47m"  # Blinking white

        BLACK_BG = "\033[40m"  # Black Background

    if os.name == "nt":
        RESET = Style.RESET_ALL

        # Red Variants
        RED_BG = Fore.LIGHTRED_EX
        BRED_BG = Fore.RED
        FRED_BG = Fore.RED
        IRED_BG = Fore.RED
        LRED_BG = Fore.LIGHTRED_EX  # Underlined RED
        URED_BG = Fore.RED  # Blinking not directly supported, using RED

        # Green Variants
        GREEN_BG = Fore.LIGHTGREEN_EX
        BGREEN_BG = Fore.GREEN
        FGREEN_BG = Fore.GREEN
        IGREEN_BG = Fore.GREEN
        LGREEN_BG = Fore.LIGHTGREEN_EX  # Underlined GREEN
        UGREEN_BG = Fore.GREEN  # Blinking not directly supported, using GREEN

        # Yellow Variants
        YELLOW_BG = Fore.LIGHTYELLOW_EX
        BYELLOW_BG = Fore.YELLOW
        FYELLOW_BG = Fore.YELLOW
        IYELLOW_BG = Fore.YELLOW
        LYELLOW_BG = Fore.LIGHTYELLOW_EX  # Underlined YELLOW
        UYELLOW_BG = Fore.YELLOW  # Blinking not directly supported, using YELLOW

        # Blue Variants
        BLUE_BG = Fore.LIGHTBLUE_EX
        BBLUE_BG = Fore.BLUE
        FBLUE_BG = Fore.BLUE
        IBLUE_BG = Fore.BLUE
        LBLUE_BG = Fore.LIGHTBLUE_EX  # Underlined BLUE
        UBLUE_BG = Fore.BLUE  # Blinking not directly supported, using BLUE

        # Magenta Variants
        MAGENTA_BG = Fore.LIGHTMAGENTA_EX
        BMAGENTA_BG = Fore.MAGENTA
        FMAGENTA_BG = Fore.MAGENTA
        IMAGENTA_BG = Fore.LIGHTMAGENTA_EX
        LMAGENTA_BG = Fore.LIGHTMAGENTA_EX  # Underlined MAGENTA
        UMAGENTA_BG = Fore.MAGENTA  # Blinking not directly supported, using MAGE

        # Cyan Variants
        CYAN_BG = Fore.LIGHTCYAN_EX
        DCYAN_BG = Fore.CYAN
        ICYAN_BG = Fore.WHITE  # Indented CYAN
        FCYAN_BG = Fore.CYAN
        LCYAN_BG = Fore.LIGHTCYAN_EX  # Underlined CYAN
        UCYAN_BG = Fore.CYAN  # Blinking not directly supported, using CYAN

        # White Variants
        BWHITE_BG = Fore.WHITE
        BBWHITE_BG = Fore.WHITE  # Blinking not directly supported, using WHITE
        WHITE_BG = Fore.WHITE
        DWHITE_BG = Fore.WHITE  # Deep white (not distinct in colorama)
        FWHITE_BG = Fore.WHITE  # Faint white (not distinct in colorama)
        IWHITE_BG = Fore.WHITE  # Indented white (not distinct in colorama)
        LWHITE_BG = Fore.WHITE  # Underlined white (not distinct in colorama)
        UWHITE_BG = Fore.WHITE  # Blinking not directly supported, using WHITE
