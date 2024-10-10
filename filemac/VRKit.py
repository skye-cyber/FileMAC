#!/usr/bin/python3
import logging
import os
import cv2
from colorama import Fore, Style, init
# import numpy as np
from tqdm import tqdm
from moviepy.editor import VideoFileClip

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


def detect_missing_frames(frames):
    ''' Implementation for missing frame detection and index them, append index
    of missing frames to a list'''
    missing_frames = []
    logger.info("Index missing frames")
    for i in tqdm(range(1, len(frames) - 1), desc="Progress"):

        if frames[i] is None:
            missing_frames.append(i)

    # Exit when no missing frames are found
    if not missing_frames:
        exit(0)
    return missing_frames


def interpolate_frame(prev_frame, next_frame):
    '''Based on number and size of missing frames use this logic to create a
dummy frame by interpolating.
    combine the frame before and after the missing frame and find the missing
frame by calculating middle weight.'''
    logger.info("Interpolating")
    return cv2.addWeighted(prev_frame, 0.5, next_frame, 0.5, 0)


def repair_video(input_path, output_path):
    logger.info("Open the file")
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        logger.error("Could not open video file.")
        return

    # Collect file metadata
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    logger.info("File info:\n"
                f"\tFrames: \033[95m{frame_count}\033[0;32m\n"
                f"\tFrame Width: \033[0;95m{width}\033[0;32m\n"
                f"\tFPS: \033[0;95m{fps}\033[0m")

    frames = []
    # Remove missing frames
    logger.info("Find missing frames and index them")
    for _ in tqdm(range(frame_count), desc="Progress"):
        ret, frame = cap.read()
        if not ret:
            frames.append(None)
        else:
            frames.append(frame)

    cap.release()

    ''' Call function to detect missing frames and decide on the method to apply
 depending on number of missing frames. If number is larger than frame_count * 0.1
remove the missing frames else interpolate.'''

    missing_frames = detect_missing_frames(frames)
    if len(missing_frames) > frame_count * 0.1:  # Arbitrary threshold for many missing frames
        frames = [f for f in frames if f is not None]
    else:
        for i in missing_frames:
            ''' Based on missing frame `i` find previous frame `frames[i-1]` and preceeding frame `frames[i+1]` wher both previous and preceeding are not missing. Use them to create the middle frame.'''
            if i > 0 and i < frame_count - 1 and frames[i-1] is not None and frames[i+1] is not None:
                frames[i] = interpolate_frame(frames[i-1], frames[i+1])
            else:
                '''Where ...'''
                frames[i] = frames[i-1] if frames[i -
                                                  1] is not None else frames[i+1]

    # Create writer objectfor the frames
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(
        *'mp4v'), fps, (width, height))

    # Write the new video to file
    for frame in frames:
        "Don't write empty frames"
        if frame is not None:
            out.write(frame)

    out.release()
    print("Video repair complete and saved to:", output_path)


# Usage
input_video_path = '/home/skye/Videos/supercar.mp4'
output_video_path = 'output_video.mp4'
repair_video(input_video_path, output_video_path)
