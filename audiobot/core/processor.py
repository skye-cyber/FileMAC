import os
from .audio.core import AudioModulator
from moviepy import AudioFileClip, VideoFileClip
from ..utils.logging_utils import colored_logger
from pydub import AudioSegment
from ..utils.visualizer import audiowave_visualizer
from ..utils.metadata_utils import get_audio_bitrate
from .effects import VoiceEffectProcessor
from filemac.utils.colors import fg, rs
import sys
# import io

RESET = rs

Clogger = colored_logger()


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

        Clogger.info(f"Set Voice effect : {fg.MAGENTA}{effect}{RESET}")
        Clogger.info(f"Processing video file: {input_file}")

        try:
            # Get the original video bitrate
            original_bitrate = get_audio_bitrate(input_file, verbosity)
            if verbosity and original_bitrate:
                Clogger.info(
                    f"Original video bitrate: {fg.YELLOW}{original_bitrate}{RESET}"
                )

            # Capture stdout and stderr
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            # sys.stdout = captured_stdout = io.StringIO()
            # sys.stderr = captured_stderr = io.StringIO()

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
                f"Applying the [{fg.BBWHITE}{effect}{RESET}{fg.GREEN}] effect"
            )
            modified_audio = VoiceEffectProcessor(audio_segment, effect).apply_effect()

            # Normalize the modified audio
            modified_audio = AudioModulator().normalize(modified_audio)

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
                    f"Set:\n\tCodec = [{fg.fg.MAGENTA}libx264{fg.GREEN}\n"
                    f"\tCodec type = [{fg.fg.MAGENTA}aac{fg.GREEN}\n"
                    f"\tBitrate = [{fg.MAGENTA}{original_bitrate or '5000k'}{RESET}]"
                )

            final_video.write_videofile(
                output_file,
                codec="libx264",
                audio_codec="aac",
                bitrate=original_bitrate or "5000k",
            )

            Clogger.info(f"Modified video saved as: {output_file}")
            Clogger.debug(f"Final bitrate = {get_audio_bitrate(output_file)}")
            # Optional: visualize the before and after audio
            if visualize:
                audiowave_visualizer(audio_file, "modified_audio.wav")

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
        Clogger.info(f"Set Voice effect : {fg.MAGENTA}{effect}{RESET}")

        Clogger.info(f"Processing audio file: {fg.MAGENTA}{input_file}{RESET}")

        try:
            audio_segment = AudioSegment.from_file(input_file)
            if verbosity:
                print(f"- INFO - Audio channels: {audio_segment.channels}")
                print(f"- INFO - Audio sample width: {audio_segment.sample_width}")
            modified_audio = VoiceEffectProcessor(audio_segment, effect).apply_effect()
            modified_audio = AudioModulator().normalize(modified_audio)
            output_file = os.path.join(
                output_dir, f"{effect}_{os.path.basename(input_file)}"
            )
            modified_audio.export(output_file, format="wav")
            Clogger.info(f"Modified audio saved as: {output_file}")

            if visualize:
                audiowave_visualizer(input_file, output_file)

        except Exception as e:
            Clogger.error(f"Error processing audio file {input_file}: {e}")
