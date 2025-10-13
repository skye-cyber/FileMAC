import os
import re
import sys
from moviepy import VideoFileClip
from pydub import AudioSegment
from tqdm.auto import tqdm
from .m4a_converter import m4a
from rich.progress import Progress
from ...utils.colors import fg, rs
from ...utils.formats import SUPPORTED_AUDIO_FORMATS_DIRECT, SUPPORTED_AUDIO_FORMATS

RESET = rs


class AudioConverter:
    """Convert Audio file to from one format to another"""

    def __init__(self, input_file, out_format):
        self.input_file = input_file
        self.out_format = out_format

    def preprocess(self):
        files_to_process = []

        if os.path.isfile(self.input_file):
            files_to_process.append(self.input_file)
        elif os.path.isdir(self.input_file):
            if os.listdir(self.input_file) is None:
                print(f"{fg.RED}Cannot work with empty folder{RESET}")
                sys.exit(1)
            for file in os.listdir(self.input_file):
                file_path = os.path.join(self.input_file, file)
                if os.path.isfile(file_path):
                    files_to_process.append(file_path)

        return files_to_process

    def pydub_conv(self):
        try:
            input_list = self.preprocess()
            out_f = self.out_format
            input_list = [
                item
                for item in input_list
                if any(item.lower().endswith(ext) for ext in SUPPORTED_AUDIO_FORMATS)
            ]
            print(f"{fg.BYELLOW}Initializing conversion..{RESET}")

            def wav_redudancy():
                # Load the mp3 file using Pydub
                audio = AudioSegment.from_file(file, fmt)
                # Export the audio to a temporary file in wav format (ffmpeg can convert from wav to m4a)
                audio.export("temp.wav", format="wav")

            for file in tqdm(input_list):
                if out_f.lower() in SUPPORTED_AUDIO_FORMATS_DIRECT:
                    _, ext = os.path.splitext(file)
                    output_filename = _ + "." + out_f
                    fmt = ext[1:]
                    # print(fmt, out_f)
                    audio = AudioSegment.from_file(file, fmt)
                    print(f"{fg.BMAGENTA}Converting to {output_filename}{RESET}")
                    audio.export(output_filename, format=out_f)
                    # new_audio = pydub.AudioSegment.from_file('output_audio.')
                    print(f"{fg.BGREEN}Done{RESET}")

                elif file[-3:].lower() == "m4a" or out_f.lower() == "m4a":
                    m4a(file, out_f)

                elif (
                    out_f.lower() in SUPPORTED_AUDIO_FORMATS
                    and not SUPPORTED_AUDIO_FORMATS_DIRECT
                ):
                    print("Pending Implemantation For the format")

                else:
                    print(f"{fg.RED}Unsupported output format{RESET}")
                    sys.exit(1)

        except KeyboardInterrupt:
            print("\nQuit❕")
            sys.exit(1)
        except Exception as e:
            print(f"{fg.RED}{e}{RESET}")


class AudioJoiner:
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
            print(f"Join {fg.BBLUE}{len(os.listdir(self.obj))}{RESET} files")

            for file in list(os.listdir(self.obj)):
                path = os.path.join(self.obj, file)
                if path.split(".")[-1] in SUPPORTED_AUDIO_FORMATS_DIRECT:
                    self.files.append(path)

        else:
            print("Pass")
            pass

    @staticmethod
    # Function to extract the number from the filename
    def extract_number(filename):
        match = re.search(r"_(\d+(\.\d+)?)\.ogg", filename)
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
                masterfile = os.path.splitext(self.files[0])[0] + "_master.ogg"
                print(os.path.splitext(self.files[0]))
            else:
                masterfile = self.masterfile
            print(f"{fg.YELLOW}Master file = {fg.BLUE}{masterfile}{RESET}")

            self.ext = os.path.splitext(masterfile)[-1]
            _format = self.ext if self.ext in SUPPORTED_AUDIO_FORMATS_DIRECT else "ogg"
            print(f"{fg.BYELLOW}Format = {fg.BBLUE}{_format}{RESET}")

            print(f"{fg.BBLUE}Create a master file{RESET}")
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
                task2 = progress.add_task(
                    "[cyan]Create list", total=len(sorted_filenames)
                )
                for i, filename in enumerate(sorted_filenames):
                    # print(f"{BWHITE}File {DCYAN}{filename}{RESET}")
                    ogg_files.append(AudioSegment.from_file(filename))
                    progress.update(task2, advance=i)

            # Concatenate the ogg files
            combined_ogg = ogg_files[0]
            with Progress() as progress:
                task3 = progress.add_task(
                    "[magenta]Joining... ", total=len(sorted_filenames)
                )
                for i in range(1, len(sorted_filenames)):
                    combined_ogg += ogg_files[i]
                    progress.update(task3, advance=i)

            # Export the combined ogg to new mp3 file or ogg file
            combined_ogg.export(masterfile, format=_format)
            print(f"{fg.BGREEN}Master file:Ok🤏")
            """
            if self.isdir:
                query = input(f"{BBLUE}Remove the directory ?(y/n)").lower() in ('y', 'yes')
                if query:
                    shutil.rmtree(self.obj)
            """
        except KeyboardInterrupt:
            print("\nQuit!")
            sys.exit(1)
        except Exception as e:
            raise
            print(f"{fg.RED}{e}{RESET}")


class AudioExtracter:
    def __init__(self, input_file):
        self.input_file = input_file

    def preprocess(self):
        try:
            files_to_process = []

            if os.path.isfile(self.input_file):
                files_to_process.append(self.input_file)
            elif os.path.isdir(self.input_file):
                if os.listdir(self.input_file) is None:
                    print(f"{fg.RED}Cannot work with empty folder{RESET}")
                    sys.exit(1)
                for file in os.listdir(self.input_file):
                    file_path = os.path.join(self.input_file, file)
                    ls = ["mp4", "mkv"]
                    if os.path.isfile(file_path) and any(
                        file_path.lower().endswith(ext) for ext in ls
                    ):
                        files_to_process.append(file_path)

            return files_to_process
        except Exception as e:
            print(e)

    def moviepyextract(self):
        try:
            video_list = self.preprocess()
            for input_video in video_list:
                print(f"{fg.BYELLOW}Extracting..{fg.DCYAN}")
                video = VideoFileClip(input_video)
                audio = video.audio
                basename, _ = os.path.splitext(input_video)
                outfile = basename + ".wav"
                audio.write_audiofile(outfile)
                # print(f"\033[1;32mFile saved as \033[36m{outfile}\033[0m")
        except KeyboardInterrupt:
            print("\nExiting..")
            sys.exit(1)
        except Exception as e:
            print(e)

    def ffmpeg_extractor(self):
        import subprocess

        video_list = self.preprocess()
        for input_video in video_list:
            # Extract audio
            subprocess.run(
                ["ffmpeg", "-i", f"{input_video}", f"{input_video.split('.')[0]}.mp3"]
            )
            # Merge audio and video
            # subprocess.run(["ffmpeg", "-i", f"{input_video}", "-i", "audio.mp3", "-c:v", "copy", "-c:a", "aac", f"{input_video}"])

    def pydub_extractor(self):
        import subprocess

        video_list = self.preprocess()
        for input_video in video_list:
            # Ensure FFmpeg is installed
            subprocess.run(["ffmpeg", "-version"])
            # Extract audio
            video = AudioSegment.from_file(f"{input_video}")
            video.export(f"{input_video.split('.')[0]}.mp3", format="mp3")
