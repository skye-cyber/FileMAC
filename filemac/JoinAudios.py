import os
import re
import sys

from pydub import AudioSegment

from .colors import (BLUE, BWHITE, DBLUE, DCYAN, DGREEN, DYELLOW,
                     RED, RESET, YELLOW)
from .formats import SUPPORTED_AUDIO_FORMATS_DIRECT


class JoinAudios:
    def __init__(self, obj, masterfile=None):
        self.obj = obj
        self.masterfile = masterfile
        self.files = []

        if os.path.exists(self.obj) and os.path.isdir(self.obj):

            print(f"Join {DBLUE}{len(os.listdir(self.obj))}{RESET} files")

            for file in list(os.listdir(self.obj)):
                # print(f"{key} ->{fl}")
                # print(f"{CYAN}Append {MAGENTA} {file}{RESET}")
                path = os.path.join(self.obj, file)
                self.files.append(path)
        elif self.obj is list:
            for file in self.obj:
                self.files.append(file)
        else:
            pass

    @staticmethod
    # Function to extract the number from the filename
    def extract_number(filename):
        match = re.search(r'_(\d+(\.\d+)?)\.ogg', filename)
        if match:
            return float(match.group(1))
        return None

    def worker(self):
        try:
            if not self.masterfile:
                masterfile = f"{os.path.splitext(self.obj)[0]}_master.ogg"
            else:
                masterfile = self.masterfile
            print(f"{YELLOW}Master file = {BLUE}{masterfile}{RESET}")

            self.ext = os.path.splitext(masterfile)[-1]
            _format = self.ext if self.ext in SUPPORTED_AUDIO_FORMATS_DIRECT else 'ogg'
            print(f"{DYELLOW}Format = {DBLUE}{_format}{RESET}")

            print(
                f"{DBLUE}Create a master file{RESET}")
            # Create a list to store files
            ogg_files = []

            # Sort the filenames based on the extracted number
            sorted_filenames = sorted(self.files, key=self.extract_number)

            # loop through the directory while adding the ogg files to the list
            for filename in sorted_filenames:
                print(f"{BWHITE}File {DCYAN}{filename}{RESET}")
                # if filename.endswith('.ogg'):
                # sys.exit()
                # ogg_file = os.path.join(path, filename)
                ogg_files.append(AudioSegment.from_file(filename))

            # Concatenate the ogg files
            combined_ogg = ogg_files[0]
            for i in range(1, len(self.files)):
                combined_ogg += ogg_files[i]

            # Export the combined ogg to new mp3 file or ogg file
            combined_ogg.export(masterfile, format=_format)
            print(F"{DGREEN}Master file:Ok🤏")
        except KeyboardInterrupt:
            print("\nQuit!")
            sys.exit(1)
        except Exception as e:
            print(f"{RED}{e}{RESET}")


if __name__ == "__main__":
    init = JoinAudios('/home/skye/Downloads/RichDad')
    init.worker()