import logging
import logging.handlers
import os
import sys

from moviepy.editor import VideoFileClip

from .colors import DCYAN, DYELLOW, RED, RESET

###############################################################################
logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


class ExtractAudio:
    def __init__(self, input_file):
        self.input_file = input_file

    def preprocess(self):
        try:
            files_to_process = []

            if os.path.isfile(self.input_file):
                files_to_process.append(self.input_file)
            elif os.path.isdir(self.input_file):
                if os.listdir(self.input_file) is None:
                    print(f"{RED}Cannot work with empty folder{RESET}")
                    sys.exit(1)
                for file in os.listdir(self.input_file):
                    file_path = os.path.join(self.input_file, file)
                    ls = ["mp4", "mkv"]
                    if os.path.isfile(file_path) and any(file_path.lower().endswith(ext) for ext in ls):
                        files_to_process.append(file_path)

            return files_to_process
        except Exception as e:
            print(e)

    def moviepyextract(self):
        try:
            video_list = self.preprocess()
            for input_video in video_list:
                print(F"{DYELLOW}Extracting..{DCYAN}")
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


if __name__ == "__main__":
    vi = ExtractAudio(
        "/home/skye/Music/Melody in My Mind.mp4")
    vi.moviepyextract()
