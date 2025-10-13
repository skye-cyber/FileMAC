import speech_recognition as sr
import ffmpeg
from .logging_utils import colored_logger
from filemac.utils.colors import fg, rs

RESET = rs

Clogger = colored_logger()


def get_audio_bitrate(input_file, verbosity=False):
    """
    Probes a media file using ffmpeg and returns its metadata.

    Args:
        input_file (str): The path to the media file.

    Returns:
        int: bitrate

    Raises:
        ffmpeg.Error: If ffmpeg returns a non-zero exit code.
        FileNotFoundError: If the input file does not exist.
        Exception: For other errors during probing.
    """
    if verbosity:
        Clogger.info(
            f"Fetch the original bitrate of the video file using {fg.YELLOW}ffmpeg{RESET}."
        )
    try:
        try:
            metadata = ffmpeg.probe(input_file)
        finally:
            bitrate = None
            # Iterate over the streams and find the video stream
            for stream in metadata["streams"]:
                if stream["codec_type"] == "video":
                    bitrate = stream.get("bit_rate", None)
                    break
            return bitrate
    except ffmpeg.Error or Exception as e:
        Clogger.error(f"Error fetching bitrate for {input_file}: {e}")
        return None


def transcribe_audio(input_file):
    Clogger.info(f"Transcribing audio: {input_file}")
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(input_file) as source:
            audio = recognizer.record(source)
        transcription = recognizer.recognize_google(audio)
        Clogger.info(f"Transcription: {transcription}")
        return transcription
    except Exception as e:
        Clogger.error(f"Error transcribing audio file {input_file}: {e}")
        return None
