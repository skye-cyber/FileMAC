import os
from .modulator import Modulator
from moviepy import AudioFileClip, VideoFileClip
from .logger_init import set_logger
from pydub import AudioSegment
from ._utils import visualize_audio, get_bitrate
from .effects import Voice
from utils.colors import DMAGENTA, RESET, YELLOW, MAGENTA, GREEN, BBWHITE
import sys
import io

logger = set_logger()


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

        logger.info(f"Voice : {DMAGENTA}{effect}{RESET}")
        logger.info(f"Processing video file: {input_file}")

        try:
            # Get the original video bitrate
            original_bitrate = get_bitrate(input_file, verbosity)
            if verbosity and original_bitrate:
                logger.info(
                    f"Original video bitrate: {YELLOW}{original_bitrate}{RESET}"
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
                logger.info("Extract audio and write it to file")
            video.audio.write_audiofile(audio_file)
            audio_segment = AudioSegment.from_file(audio_file)

            # Apply the selected voice effect
            logger.info(f"Applying the [{BBWHITE}{effect}{RESET}{GREEN}] effect")
            modified_audio = Voice(audio_segment, effect).apply_effect()

            # Normalize the modified audio
            modified_audio = Modulator().normalize(modified_audio)

            # Export the modified audio to a WAV file
            if verbosity:
                logger.info("Export the modified audio to a WAV file")
            modified_audio.export("modified_audio.wav", format="wav")

            # Load the modified audio file back into an AudioFileClip
            new_audio = AudioFileClip("modified_audio.wav")

            # Set the video to use the modified audio
            if verbosity:
                logger.info("Set the video audio to the new modified audio")
            final_video = video.with_audio(new_audio)

            # Define the output file path
            output_file = os.path.join(
                output_dir, f"{effect}_{os.path.basename(input_file)}"
            )

            # Use the original bitrate or default to 5000k if unavailable
            if verbosity:
                logger.info(
                    f"Set:\n\tCodec = [{MAGENTA}libx264{GREEN}\n"
                    f"\tCodec type = [{MAGENTA}aac{GREEN}\n"
                    f"\tBitrate = [{MAGENTA}{original_bitrate or '5000k'}{RESET}]"
                )

            final_video.write_videofile(
                output_file,
                codec="libx264",
                audio_codec="aac",
                bitrate=original_bitrate or "5000k",
            )

            logger.info(f"Modified video saved as: {output_file}")
            logger.debug(f"Final bitrate = {get_bitrate(output_file)}")
            # Optional: visualize the before and after audio
            if visualize:
                visualize_audio(audio_file, "modified_audio.wav")

            # Clean up temporary files
            if os.path.exists(audio_file):
                os.remove(audio_file)
                os.remove("modified_audio.wav")

        except KeyboardInterrupt:
            logger.info("Quit")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error processing video file {input_file}: {e}")
            # raise


class AudioProcessor:
    def __init__(self):
        pass

    def process_audio_file(
        self, input_file, effect, output_dir, verbosity, visualize=False
    ):
        logger.info(f"Voice : {DMAGENTA}{effect}{RESET}")

        logger.info(f"Processing audio file: {input_file}")

        try:
            audio_segment = AudioSegment.from_file(input_file)
            if verbosity:
                print(f"- INFO - Audio channels: {audio_segment.channels}")
                print(f"- INFO - Audio sample width: {audio_segment.sample_width}")
            modified_audio = Voice(audio_segment, effect).apply_effect()
            modified_audio = Modulator().normalize(modified_audio)
            output_file = os.path.join(
                output_dir, f"{effect}_{os.path.basename(input_file)}"
            )
            modified_audio.export(output_file, format="wav")
            logger.info(f"Modified audio saved as: {output_file}")

            if visualize:
                visualize_audio(input_file, output_file)

        except Exception as e:
            # raise
            logger.error(f"Error processing audio file {input_file}: {e}")
