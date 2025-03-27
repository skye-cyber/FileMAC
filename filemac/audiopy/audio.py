import os
import sys

import pydub
from tqdm import tqdm

from utils.colors import foreground
from ..audiopy.m4a_converter import m4a
from utils.formats import SUPPORTED_AUDIO_FORMATS, SUPPORTED_AUDIO_FORMATS_DIRECT

###############################################################################
# Convert Audio file to from one format to another'''
###############################################################################

fcl = foreground()
RESET = fcl.RESET


class AudioConverter:
    def __init__(self, input_file, out_format):
        self.input_file = input_file
        self.out_format = out_format

    def preprocess(self):
        files_to_process = []

        if os.path.isfile(self.input_file):
            files_to_process.append(self.input_file)
        elif os.path.isdir(self.input_file):
            if os.listdir(self.input_file) is None:
                print(f"{fcl.RED_FG}Cannot work with empty folder{RESET}")
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
            print(f"{fcl.BYELLOW_FG}Initializing conversion..{RESET}")

            def wav_redudancy():
                # Load the mp3 file using Pydub
                audio = pydub.AudioSegment.from_file(file, fmt)
                # Export the audio to a temporary file in wav format (ffmpeg can convert from wav to m4a)
                audio.export("temp.wav", format="wav")

            for file in tqdm(input_list):
                if out_f.lower() in SUPPORTED_AUDIO_FORMATS_DIRECT:
                    _, ext = os.path.splitext(file)
                    output_filename = _ + "." + out_f
                    fmt = ext[1:]
                    # print(fmt, out_f)
                    audio = pydub.AudioSegment.from_file(file, fmt)
                    print(f"{fcl.BMAGENTA_FG}Converting to {output_filename}{RESET}")
                    audio.export(output_filename, format=out_f)
                    # new_audio = pydub.AudioSegment.from_file('output_audio.')
                    print(f"{fcl.BGREEN_FG}Done{RESET}")

                elif file[-3:].lower() == "m4a" or out_f.lower() == "m4a":
                    m4a(file, out_f)

                elif (
                    out_f.lower() in SUPPORTED_AUDIO_FORMATS
                    and not SUPPORTED_AUDIO_FORMATS_DIRECT
                ):
                    print("Pending Implemantation For the format")

                else:
                    print(f"{fcl.RED_FG}Unsupported output format{RESET}")
                    sys.exit(1)

        except KeyboardInterrupt:
            print("\nQuit❕")
            sys.exit(1)
        except Exception as e:
            print(f"{fcl.RED_FG}{e}{RESET}")
