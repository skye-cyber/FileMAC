import os
from .modulator import Modulator
from moviepy import AudioFileClip, VideoFileClip
from .logging_config import setup_colored_logger
from pydub import AudioSegment
from .audioutils.visualizer import visualize_audio_wave
from .audioutils.utils import get_bitrate
from .effects import VoiceEffectProcessor
from utils.colors import foreground
import sys
import io

fcl = foreground()
RESET = fcl.RESET

Clogger = setup_colored_logger()


class VideoProcessor:
    def __init__(self):
        pass

    def process_video_file(
        self,
        input_file,
        effect,
        output_dir,
        verbosity: bool = False,
        visualize: bool = False,
    ):
        """
        Process video file by applying audio effects and retaining original bitrate.
        """

        Clogger.info(f"Set Voice effect : {fcl.MAGENTA_FG}{effect}{RESET}")
        Clogger.info(f"Processing video file: {input_file}")

        try:
            # Get the original video bitrate
            original_bitrate = get_bitrate(input_file, verbosity)
            if verbosity and original_bitrate:
                Clogger.info(
                    f"Original video bitrate: {fcl.YELLOW_FG}{original_bitrate}{RESET}"
                )

            # Capture stdout and stderr
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = captured_stdout = io.StringIO()
            sys.stderr = captured_stderr = io.StringIO()

            # Load the video
            try:
                video = VideoFileClip(input_file)
            finally:
                sys.stdout = old_stdout  # Restore stdout
                sys.stderr = old_stderr  # Restore stder
                audio_file = "temp_audio.wav"

            # Extract audio and save it to a file
            if verbosity:
                Clogger.info("Extract audio and write it to file")
            video.audio.write_audiofile(audio_file)
            audio_segment = AudioSegment.from_file(audio_file)

            # Apply the selected voice effect
            Clogger.info(
                f"Applying the [{fcl.BBWHITE_FG}{effect}{RESET}{fcl.GREEN_FG}] effect"
            )
            modified_audio = VoiceEffectProcessor(audio_segment, effect).apply_effect()

            # Normalize the modified audio
            modified_audio = Modulator().normalize(modified_audio)

            # Export the modified audio to a WAV file
            if verbosity:
                Clogger.info("Export the modified audio to a WAV file")
            modified_audio.export("modified_audio.wav", format="wav")

            # Load the modified audio file back into an AudioFileClip
            new_audio = AudioFileClip("modified_audio.wav")

            # Set the video to use the modified audio
            if verbosity:
                Clogger.info("Set the video audio to the new modified audio")
            final_video = video.with_audio(new_audio)

            # Define the output file path
            output_file = os.path.join(
                output_dir, f"{effect}_{os.path.basename(input_file)}"
            )

            # Use the original bitrate or default to 5000k if unavailable
            if verbosity:
                Clogger.info(
                    f"Set:\n\tCodec = [{fcl.fcl.MAGENTA_FG}libx264{fcl.GREEN_FG}\n"
                    f"\tCodec type = [{fcl.fcl.MAGENTA_FG}aac{fcl.GREEN_FG}\n"
                    f"\tBitrate = [{fcl.MAGENTA_FG}{original_bitrate or '5000k'}{RESET}]"
                )

            final_video.write_videofile(
                output_file,
                codec="libx264",
                audio_codec="aac",
                bitrate=original_bitrate or "5000k",
            )

            Clogger.info(f"Modified video saved as: {output_file}")
            Clogger.debug(f"Final bitrate = {get_bitrate(output_file)}")
            # Optional: visualize the before and after audio
            if visualize:
                visualize_audio_wave(audio_file, "modified_audio.wav")

            # Clean up temporary files
            if os.path.exists(audio_file):
                os.remove(audio_file)
                os.remove("modified_audio.wav")

        except KeyboardInterrupt:
            Clogger.info("Quit")
            sys.exit(1)
        except Exception as e:
            Clogger.error(f"Error processing video file {input_file}: {e}")
            # raise


class AudioProcessor:
    def __init__(self):
        pass

    def process_audio_file(
        self, input_file, effect, output_dir, verbosity, visualize=False
    ):
        Clogger.info(f"Set Voice effect : {fcl.MAGENTA_FG}{effect}{RESET}")

        Clogger.info(f"Processing audio file: {fcl.MAGENTA_FG}{input_file}{RESET}")

        try:
            audio_segment = AudioSegment.from_file(input_file)
            if verbosity:
                print(f"- INFO - Audio channels: {audio_segment.channels}")
                print(f"- INFO - Audio sample width: {audio_segment.sample_width}")
            modified_audio = VoiceEffectProcessor(audio_segment, effect).apply_effect()
            modified_audio = Modulator().normalize(modified_audio)
            output_file = os.path.join(
                output_dir, f"{effect}_{os.path.basename(input_file)}"
            )
            modified_audio.export(output_file, format="wav")
            Clogger.info(f"Modified audio saved as: {output_file}")

            if visualize:
                visualize_audio_wave(input_file, output_file)

        except Exception as e:
            Clogger.error(f"Error processing audio file {input_file}: {e}")
