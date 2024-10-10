#!/usr/bin/python3
import logging
import os

import cv2
from colorama import Fore, Style, init
from moviepy.editor import AudioFileClip, VideoFileClip
# import numpy as np
from tqdm import tqdm

# Initialize colorama
init(autoreset=True)

# Custom formatter class to add colors


class CustomFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, Fore.WHITE)
        log_message = super().format(record)
        return f"{log_color}{log_message}{Style.RESET_ALL}"


# Set up logging
logger = logging.getLogger("colored_logger")
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter("- %(levelname)s - %(message)s"))

logger.addHandler(handler)
logger.setLevel(logging.INFO)


class AudioMan():

    def __init__(self, obj):
        self.obj = obj
        # Load the video file
        self.video = VideoFileClip(self.obj)
        basename, _ = os.path.splitext(self.obj)
        self.outfile = basename + ".wav"

    def Extract_audio(self):
        # audio = video.audio
        self.video.audio.write_audiofile(self.outfile)

    def Write_audio(self, outfile):
        # Load the audio file
        audio = AudioFileClip(outfile)
        new = self.video.set_audio(audio)
        # Export the final video
        return new.write_videofile("output_@vkitpro.mp4", codec="libx264", audio_codec="aac", bitrate="125.4k")


class VideoRepair:
    def __init__(self, obj):
        self.obj = obj

        logger.info("Open the file")
        self.cap = cv2.VideoCapture(obj)
        if not self.cap.isOpened():
            logger.error("Could not open video file.")
            return

        # Collect file metadata
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)

        logger.info("File info:\n"
                    f"\tFrames: \033[95m{self.frame_count}\033[0;32m\n"
                    f"\tFrame Width: \033[0;95m{width}\033[0;32m\n"
                    f"\tFrame Height: \033[0;95m{height}\033[0;32m\n"
                    f"\tFPS: \033[0;95m{fps}\033[0m")

    def get_frame_size_in_bytes(frame):
        return frame.nbytes  # Get the size of the frame in bytes

    def Repair(self, batch: int = 2):
        logger.info("Find missing frames and index them")
        batch_size = batch * 1024 * 1024
        l_frame = None
        r_frame = None
        current_batch_size = 0
        frames_batch = []

        for _ in tqdm(range(self.frame_count), desc="Progress"):
            ret, frame = self.cap.read()
            if not ret:
                # If no frame is captured, break the loop
                self.frames.append(None)
            else:
                self.frames.append(frame)

        self.cap.release()


class cv2Repair:
    def __init__(self)
    self = self

    def preprocessor(input_video_path):
        cap = cv2.VideoCapture(input_video_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                pass
            else:
                yield frame  # Yield frame one by one (lazy loading)

        cap.release()

    def repair
        # Process the frames using the generator
        for frame in tqdm(preprocessor('/home/skye/Videos/FixedSupercar.mp4')):
            run = AudioMan()
            run.Write_audio()

if __name__ == "__main__":
    run = AudioMan("/home/skye/Videos/FixedSupercar.mp4")
    run.Write_audio("/home/skye/Videos/supercar.wav")
