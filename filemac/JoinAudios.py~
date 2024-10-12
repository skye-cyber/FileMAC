import os
import re
import sys
import shutil
from pydub import AudioSegment
from rich.progress import Progress
from .colors import (BLUE, BWHITE, DBLUE, DCYAN, DGREEN, DYELLOW,
                     RED, RESET, YELLOW)
from .formats import SUPPORTED_AUDIO_FORMATS_DIRECT


class JoinAudios:
    def __init__(self, obj: list, masterfile=None):
        self.obj = obj
        self.masterfile = masterfile
        self.files = []

        if isinstance(self.obj, list):
            self.isdir = False
            for file in self.obj:
                self.files.append(file)

        elif os.path.isdir(self.obj):
            self.obj = self.obj
            self.isdir = True
            print(f"Join {DBLUE}{len(os.listdir(self.obj))}{RESET} files")

            for file in list(os.listdir(self.obj)):
                path = os.path.join(self.obj, file)
                if path.split('.')[-1] in SUPPORTED_AUDIO_FORMATS_DIRECT:
                    self.files.append(path)

        else:
            print("Pass")
            pass

    @staticmethod
    # Function to extract the number from the filename
    def extract_number(filename):
        match = re.search(r'_(\d+(\.\d+)?)\.ogg', filename)
        if match:
            try:
                return float(match.group(1))
            except TypeError:
                return int(match.group(1))
        else:
            return 0

    def worker(self):
        try:
            if len(self.files) == 0:
                print("No files to work on")
                print("\nQuit!")
                exit(0)
            if self.masterfile is None:
                masterfile = os.path.splitext(self.files[0])[0] + '_master.ogg'
                print(os.path.splitext(self.files[0]))
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
            _sorted_filenames = sorted(self.files, key=self.extract_number)

            print("." * 20, "Remove Empty files", "." * 20)
            sorted_filenames = []
            with Progress() as progress:
                task = progress.add_task("[magenta]Preparing..", total=None)
                for i, fl in enumerate(_sorted_filenames):
                    if os.path.getsize(fl) == 0:
                        print("Empty file, skipping..")
                        continue
                    else:
                        sorted_filenames.append(fl)
                    progress.update(task, advance=None)

            # loop through the directory while adding the ogg files to the list
            with Progress() as progress:
                task2 = progress.add_task("[cyan]Create list", total=len(sorted_filenames))
                for i, filename in enumerate(sorted_filenames):
                    # print(f"{BWHITE}File {DCYAN}{filename}{RESET}")
                    ogg_files.append(AudioSegment.from_file(filename))
                    progress.update(task2, advance=i)

            # Concatenate the ogg files
            combined_ogg = ogg_files[0]
            with Progress() as progress:
                task3 = progress.add_task("[magenta]Joining... ", total=len(sorted_filenames))
                for i in range(1, len(sorted_filenames)):
                    combined_ogg += ogg_files[i]
                    progress.update(task3, advance=i)

            # Export the combined ogg to new mp3 file or ogg file
            combined_ogg.export(masterfile, format=_format)
            print(F"{DGREEN}Master file:Ok🤏")
            """
            if self.isdir:
                query = input(f"{DBLUE}Remove the directory ?(y/n)").lower() in ('y', 'yes')
                if query:
                    shutil.rmtree(self.obj)
            """
        except KeyboardInterrupt:
            print("\nQuit!")
            sys.exit(1)
        except Exception as e:
            raise
            print(f"{RED}{e}{RESET}")


if __name__ == "__main__":
    init = JoinAudios('/home/skye/Downloads/RichDad')
    init.worker()
