###############################################################################
# Convert video file to from one format to another'''
###############################################################################
import os
import subprocess
import sys

import cv2
from moviepy import VideoFileClip
from pydub import AudioSegment
from tqdm import tqdm

from utils.colors import foreground, background
from utils.formats import SUPPORTED_VIDEO_FORMATS, Video_codecs

fcl = foreground()
bcl = background()
RESET = fcl.RESET


class VideoConverter:
    def __init__(self, input_file, out_format=None):
        self.input_file = input_file
        self.out_format = out_format

    def preprocess(self):
        if self.out_format is None:
            return None
        files_to_process = []

        if os.path.isfile(self.input_file):
            files_to_process.append(self.input_file)
        elif os.path.isdir(self.input_file):
            if os.listdir(self.input_file) is None:
                print(f"{bcl.RED_BG}Cannot work with empty folder{RESET}")
                sys.exit(1)
            for file in os.listdir(self.input_file):
                file_path = os.path.join(self.input_file, file)
                if os.path.isfile(file_path):
                    files_to_process.append(file_path)

        return files_to_process

    def ffmpeg_merger(self, obj: list = None):
        video_list = self.preprocess(), obj
        for input_video in video_list:
            base, ext = input_video.split(".", 1)
            output_file = f"{base}_new_.{ext}"

            # keep the original video quality by using -c:v copy, which avoids re-encoding.
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    input_video,
                    "-i",
                    "audio.mp3",
                    "-c:v",
                    "copy",
                    "-c:a",
                    "aac",
                    "-strict",
                    "experimental",
                    output_file,
                ]
            )

    def pydub_merger(self, obj: list = None):
        video_list = self.preprocess() or obj
        for input_video in video_list:
            output_file = [f"{_}_new_.{ext}" for _, ext in [input_video.split(".", 1)]][
                0
            ]
            # Process or manipulate audio with Pydub (e.g., adjust volume)
            audio = AudioSegment.from_file("audio.mp3")
            audio = audio + 6  # Increase volume by 6 dB
            audio.export("processed_audio.mp3", format="mp3")

            # Merge processed audio with video using FFmpeg
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    input_video,
                    "-i",
                    "processed_audio.mp3",
                    "-c:v",
                    "copy",
                    "-c:a",
                    "aac",
                    output_file,
                ]
            )

    def cv2_merger(self, obj: list = None):
        video_list = self.preprocess(), obj
        for input_video in video_list:
            # Read video and save frames (without audio)
            cap = cv2.VideoCapture(input_video)

            # Retrieve width and height from the video
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))

            # _, ext = input_video.split('.')[0]
            # output_file = f"{_}_new{ext}"
            output_file = [f"{_}_new_.{ext}" for _, ext in [input_video.split(".", 1)]][
                0
            ]
            # Define the VideoWriter with the video dimensions
            out = cv2.VideoWriter(
                output_file, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
            )

            # Read frames from the original video and write them to the output
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)

            # Release resources
            cap.release()
            out.release()

            # Merge with audio using FFmpeg
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    "video_no_audio.mp4",
                    "-i",
                    "audio.mp3",
                    "-c:v",
                    "copy",
                    "-c:a",
                    "aac",
                    output_file,
                ]
            )

    def CONVERT_VIDEO(self):
        try:
            input_list = self.preprocess()
            out_f = self.out_format.upper()
            input_list = [
                item
                for item in input_list
                if any(item.upper().endswith(ext) for ext in SUPPORTED_VIDEO_FORMATS)
            ]
            print(f"{fcl.BYELLOW_FG}Initializing conversion..{RESET}")

            for file in tqdm(input_list):
                if out_f.upper() in Video_codecs.keys():
                    _, ext = os.path.splitext(file)
                    output_filename = _ + "." + out_f.lower()
                    # print(output_filename)
                elif (
                    out_f.upper() in SUPPORTED_VIDEO_FORMATS
                    and out_f.upper() not in Video_codecs.keys()
                ):
                    print(
                        f"{fcl.RED_FG}Unsupported output format --> Pending Implementation{RESET}"
                    )
                    sys.exit(1)
                else:
                    print(f"{fcl.RED_FG}Unsupported output format{RESET}")
                    sys.exit(1)

                """Load the video file"""
                print(f"{fcl.BBLUE_FG}Load file{RESET}")
                video = VideoFileClip(file)
                """Export the video to a different format"""
                print(f"{fcl.BMAGENTA_FG}Converting file to {output_filename}{RESET}")
                video.write_videofile(output_filename, codec=Video_codecs[out_f])
                """Close the video file"""
                print(f"{fcl.BGREEN_FG}Done{RESET}")
                video.close()
        except KeyboardInterrupt:
            print("\nQuit❕")
            sys.exit(1)
        except Exception as e:
            print(e)
