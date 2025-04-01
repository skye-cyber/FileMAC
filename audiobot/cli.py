#!/usr/bin/python3
import argparse
import logging

import os

import magic
from .audioutils.utils import transcribe_audio
from utils.colors import foreground
from .processor import VideoProcessor, AudioProcessor
from .logging_config import setup_colored_logger
from .config import Config

fcl = foreground()
RESET = fcl.RESET

Clogger = setup_colored_logger()


class Processor:
    def __init__(self, args, parser):
        self.args = args
        self.parser = parser
        self.mime = magic.Magic(mime=True)
        self.output_dir = os.getcwd() if not self.args.output else self.args.output

    def process(self):
        if not self.args or self.args.audio_effect:
            self.parser.print_help()
            return

        if self.args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        if self.args.output and not os.path.exists(self.args.output):
            os.makedirs(self.args.output)
        if self.args.batch:
            self.batch_processor()
        else:
            self.mono_processor()

    def mono_processor(self):
        try:
            file_type = self.mime.from_file(self.args.file)
            Clogger.info(f"{fcl.BLUE_FG}Detected file type: {file_type}{RESET}")
            if file_type.startswith("audio"):
                if self.args.transcribe:
                    transcribe_audio(self.args.file)
                AudioProcessor().process_audio_file(
                    self.args.file,
                    self.args.effect,
                    self.output_dir,
                    self.args.verbose,
                    self.args.visualize,
                )
            elif file_type.startswith("video"):
                VideoProcessor().process_video_file(
                    self.args.file,
                    self.args.effect,
                    self.output_dir,
                    self.args.verbose,
                    self.args.visualize,
                )
            else:
                Clogger.warning(
                    f"Unsupported file type: {file_type}. Only audio and video files are supported."
                )
        except Exception as e:
            Clogger.error(e)

    def batch_processor(self):
        try:
            for root, _, files in os.walk(self.args.file):
                for file in files:
                    full_path = os.path.join(root, file)
                    file_type = self.mime.from_file(full_path)
                    Clogger.info(f"{fcl.BLUE_FG}Detected file type: {file_type}{RESET}")
                    if file_type.startswith("audio"):
                        if self.args.transcribe:
                            transcribe_audio(full_path)
                        AudioProcessor().process_audio_file(
                            full_path,
                            self.args.effect,
                            self.output_dir,
                            self.args.verbose,
                            self.args.visualize,
                        )
                    elif file_type.startswith("video"):
                        VideoProcessor().process_video_file(
                            full_path,
                            self.args.effect,
                            self.output_dir,
                            self.args.verbose,
                            self.args.visualize,
                        )
                    else:
                        Clogger.warning(f"Ignoring unsupported file type: {file}")
        except Exception as e:
            Clogger.info(e)


def Argsmain(argsv=None):
    """
    Recieve and process agruments from audio/video audio effects
    """
    parser = argparse.ArgumentParser(
        description="Audiobot: A tool for audio effects on audio and video files.",
        usage="filemac --audio_effect [-h] [--file FILE] \n\
            [-e {robotic,deep,high,echo,reverb,whisper,demonic,chipmunk,hacker,lowpass,distortion}] \n\
            [-o OUTPUT] [-v] [-b] [--visualize] [--transcribe] \n\
            [--audio_effect]",
    )
    parser.add_argument(
        "file",
        help=f"{fcl.CYAN_FG}The input audio, video file, or directory.{RESET}",
    )
    parser.add_argument(
        "-e",
        "--effect",
        choices=[
            "robotic",
            "deep",
            "high",
            "echo",
            "reverb",
            "whisper",
            "demonic",
            "chipmunk",
            "hacker",
            "lowpass",
            "highpass",
            "distortion",
            "denoise",
        ],
        help=f"{fcl.CYAN_FG}The voice effect to apply.{RESET}",
    )
    parser.add_argument(
        "--cutoff",
        type=int,
        help=f"Cutoff frequency for denoise operation, defualt={fcl.YELLOW_FG}200{RESET}",
    )
    parser.add_argument(
        "-N",
        "--noise",
        choices=["low", "high", "both"],
        type=str,
        default="low",
        help=f"Specifies the type of noise to remove choices:[{fcl.BLUE_FG}low, high, both{RESET}] defualt={fcl.YELLOW_FG}low{RESET}",
    )
    parser.add_argument(
        "-o",
        "--output",
        help=f"{fcl.CYAN_FG}Output directory for modified files.{RESET}",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help=f"{fcl.CYAN_FG}Increase output verbosity.{RESET}",
    )
    parser.add_argument(
        "-b",
        "--batch",
        action="store_true",
        help=f"{fcl.CYAN_FG}Batch process all files in a directory.{RESET}",
    )
    parser.add_argument(
        "--visualize",
        action="store_true",
        help=f"{fcl.CYAN_FG}Visualize the audio waveform before and after modification.{RESET}",
    )
    parser.add_argument(
        "--transcribe",
        action="store_true",
        help=f"{fcl.CYAN_FG}Transcribe the audio content before applying the effect.{RESET}",
    )
    parser.add_argument("--audio_effect", action="store_true", help=argparse.SUPPRESS)

    args = parser.parse_args(argsv) if argsv else parser.parse_args()
    if args.cutoff:
        config = Config()
        config.options["cutoff"] = args.cutoff
        config.options["noise"] = args.noise
    # Call argument processor
    Processor(args, parser).process()


if __name__ == "__main__":
    Argsmain()
