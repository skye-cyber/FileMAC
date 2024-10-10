#!/usr/bin/python3
import argparse
import logging
# import mimetypes
import os
import sys

import ffmpeg
import librosa
import magic
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
import speech_recognition as sr
from colorama import Fore, Style, init
from moviepy.editor import AudioFileClip, VideoFileClip
from pydub import AudioSegment, effects
from scipy.signal import butter, lfilter

from colors import (CYAN, RESET)

# Initialize colorama
# Requires: ffmpeg-python

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
logger.setLevel(logging.DEBUG)


def pitch_shift(audio_segment, n_steps):
    # Convert the audio samples to a NumPy array in float32
    samples = np.array(audio_segment.get_array_of_samples(), dtype=np.float32)

    # If the audio is stereo, convert it to mono
    if audio_segment.channels == 2:
        samples = audio_segment.set_channels(1)

    # Convert the samples back to NumPy array and flaoting point
    samples = np.array(audio_segment.get_array_of_samples(), dtype=np.float32)

    # Pitch shift (no need to pass sample_rate separately)
    shifted_samples = librosa.effects.pitch_shift(
        samples, sr=audio_segment.frame_rate, n_steps=n_steps)

    # Convert the shifted samples back to int16
    shifted_audio = AudioSegment(
        shifted_samples.astype(np.int16).tobytes(),
        frame_rate=audio_segment.frame_rate,
        sample_width=audio_segment.sample_width,
        channels=audio_segment.channels
    )

    return shifted_audio


def hacker_voice(audio_segment):
    """Applies a deep, robotic voice effect used for anonymity."""

    # Step 1: Pitch shift down (lower the pitch)
    logger.info("Applying deep pitch shift for hacker voice")
    deep_voice = pitch_shift(audio_segment, n_steps=-10)

    # Step 2: Speed up for robotic effect
    logger.info("Speeding up for robotic effect")
    robotic_voice = effects.speedup(deep_voice, playback_speed=1.1)
    if robotic_voice is None:
        logger.error("Speedup failed")
        return None

    # Step 3: Apply reverb (check for validity)
    logger.info("Adding subtle echo for distortion")
    if isinstance(robotic_voice, AudioSegment):
        # Shorter delay for subtle echo
        delay = AudioSegment.silent(duration=500)

        logger.info("Overlaying echo effect")

        try:
            echo_effect = robotic_voice.overlay(delay + robotic_voice - 5000)
        except Exception as e:
            logger.error(f"Error during overlay: {e}")
            return None
    else:
        logger.error("Robotic voice generation failed")
        return None

    # Step 4: Apply low-pass filter (optional)
    hacker_voice_effect = effects.low_pass_filter(
        echo_effect, cutoff=2500) if echo_effect else None
    if hacker_voice_effect is None:
        logger.error("Low pass filter failed")
        return None

    return hacker_voice_effect


def apply_echo(samples, delay=0.2, decay=0.5, sample_rate=44100):
    """Apply echo effect with a specified delay and decay."""
    delay_samples = int(sample_rate * delay)
    echo_signal = np.zeros(len(samples) + delay_samples)

    echo_signal[:len(samples)] = samples
    echo_signal[delay_samples:] += decay * samples  # Delayed echo signal

    return echo_signal[:len(samples)]  # Truncate to original length


def apply_reverb(samples, decay=0.7, delay=0.05, sample_rate=44100):
    try:
        """Apply a reverb effect by adding delayed and attenuated copies of the signal."""
        delay_samples = int(sample_rate * delay)

        # Create a delayed version of the samples and attenuate (apply decay)
        reverb_samples = np.zeros_like(samples)

        if samples.ndim == 2:  # Stereo
            for i in range(delay_samples, len(samples)):
                reverb_samples[i, 0] = samples[i, 0] + \
                    decay * samples[i - delay_samples, 0]
                reverb_samples[i, 1] = samples[i, 1] + \
                    decay * samples[i - delay_samples, 1]
        else:  # Mono
            for i in range(delay_samples, len(samples)):
                reverb_samples[i] = samples[i] + \
                    decay * samples[i - delay_samples]

        return reverb_samples
    except Exception as e:
        logger.error(e)
        # raise


def apply_lowpass_filter(samples, cutoff=200, sample_rate=44100):
    """Apply a low-pass filter to remove frequencies higher than cutoff.
for voice cutoff = 1000-2000 Hz
    music cutoff = 5000-8000 Hz
    hiss/noise removal cutoff = 200-500 Hz"""
    logger.info(
        "Apply a low-pass filter to remove frequencies higher than cutoff")
    nyquist = 0.5 * sample_rate
    normal_cutoff = cutoff / nyquist
    b, a = butter(6, normal_cutoff, btype='low', analog=False)
    filtered_samples = lfilter(b, a, samples)

    return filtered_samples


def apply_distortion(samples, gain=20, threshold=0.3):
    """Apply distortion by clipping the waveform."""
    logger.info("Apply distortion by clipping the waveform.")
    samples = samples * gain
    samples = np.clip(samples, -threshold, threshold)  # Clip at threshold
    return samples


class Handle_np_segments:
    def __init__(self):
        """This class will convert:
    1.Audiosegmnents to numpy array
    2.Numpy array to audiosegment"""
        self = self

    def numpy_to_audiosegment(self, samples, sample_rate, sample_width, channels):
        """
        Converts a numpy array back to a pydub AudioSegment.
        """
        # Flatten the array if it has 2 channels (stereo)
        if len(samples.shape) == 2 and channels == 2:
            samples = samples.flatten()

        # Convert the numpy array to raw audio data
        raw_data = samples.tobytes()

        # Create a new AudioSegment using the raw audio data
        return AudioSegment(
            data=raw_data,
            sample_width=sample_width,
            frame_rate=sample_rate,
            channels=channels
        )

    def audiosegment_to_numpy(self, audio_segment):
        """
        Converts a pydub AudioSegment to a numpy array.
        Returns the numpy array and the sample rate.
        """
        samples = np.array(audio_segment.get_array_of_samples())

        # If stereo, reshape to (n_samples, 2)
        if audio_segment.channels == 2:
            samples = samples.reshape((-1, 2))

        return samples, audio_segment.frame_rate


def apply_voice_effect(audio_segment, effect, verbosity=False):

    handler = Handle_np_segments()

    # OK 1.2
    if effect == "robotic":
        return pitch_shift(effects.speedup(audio_segment, 1.01), n_steps=-10)

    # OK
    elif effect == "deep":
        return pitch_shift(audio_segment, n_steps=-4)

    # OK
    elif effect == "high":
        return pitch_shift(audio_segment, n_steps=4)

    # OK
    elif effect == "chipmunk":
        return pitch_shift(effects.speedup(audio_segment, 1.01), n_steps=9)

    elif effect == "demonic":
        return pitch_shift(effects.speedup(audio_segment, 1.01), n_steps=-10).overlay(AudioSegment.silent(duration=700) + audio_segment.fade_out(500))
        # return seg.overlay(pitch_shift(effects.speedup(audio_segment, 1.01), n_steps=11).overlay(AudioSegment.silent(duration=250) + audio_segment.fade_out(2000)))

    # OK
    elif effect == "echo":
        delay = AudioSegment.silent(duration=1000)  # 1000ms of silence
        return audio_segment.overlay(delay + audio_segment)

    # OK
    elif effect == "reverb":
        # Convert to numpy array

        samples, sample_rate = handler.audiosegment_to_numpy(
            audio_segment)

        # Apply the reverb effect
        samples = apply_reverb(samples)

        # Convert back to AudioSegment
        processed_audio = handler.numpy_to_audiosegment(
            samples, sample_rate, audio_segment.sample_width, audio_segment.channels)

        return processed_audio
        # Simple reverb effect
        # delay = AudioSegment.silent(duration=150)  # 150ms of silence
        # return audio_segment.overlay(delay + audio_segment.fade_out(3000))

    elif effect == "whisper":
        return effects.low_pass_filter(audio_segment, 70).apply_gain(-10)

    # OK
    elif effect == "hacker":
        return hacker_voice(audio_segment)

    elif effect == 'distortion':
        # Convert to numpy array
        samples, sample_rate = handler.audiosegment_to_numpy(
            audio_segment)

        # Apply the distortion effect
        samples = apply_distortion(samples)

        # Convert back to AudioSegment
        processed_audio = handler.numpy_to_audiosegment(
            samples, sample_rate, audio_segment.sample_width, audio_segment.channels)

        return processed_audio

    # OK
    elif effect == 'lowpass':
        # processed_audio
        return effects.low_pass_filter(audio_segment, cutoff=2200)

    else:
        if verbosity:
            logger.critical(f"Unknown voice effect: {effect}")
            # raise ValueError(f"Unknown voice effect: {effect}")


def normalize_audio(audio_segment):
    return effects.normalize(audio_segment)


def process_audio_file(input_file, effect, output_dir, verbosity, visualize=False):

    logger.info(f"Voice : \033[1;95m{effect}\033[0m")

    logger.info(f"Processing audio file: {input_file}")

    try:
        audio_segment = AudioSegment.from_file(input_file)
        if verbosity:
            print(f"- INFO - Audio channels: {audio_segment.channels}")
            print(f"- INFO - Audio sample width: {audio_segment.sample_width}")
        modified_audio = apply_voice_effect(audio_segment, effect)
        modified_audio = normalize_audio(modified_audio)
        output_file = os.path.join(
            output_dir, f"{effect}_{os.path.basename(input_file)}")
        modified_audio.export(output_file, format="wav")
        logger.info(f"Modified audio saved as: {output_file}")

        if visualize:
            visualize_audio(input_file, output_file)

    except Exception as e:
        # raise
        logger.error(f"Error processing audio file {input_file}: {e}")


def get_bitrate(input_file, verbosity=False):
    """Fetch the original bitrate of the video file using ffmpeg."""
    if verbosity:
        logger.info(
            "Fetch the original bitrate of the video file using ffmpeg.")
    try:
        probe = ffmpeg.probe(input_file)
        bitrate = None
        # Iterate over the streams and find the video stream
        for stream in probe['streams']:
            if stream['codec_type'] == 'video':
                bitrate = stream.get('bit_rate', None)
                break
        return bitrate
    except ffmpeg.Error as e:
        logger.error(f"Error fetching bitrate for {input_file}: {e}")
    except Exception as e:
        logger.error(f"Error fetching bitrate for {input_file}: {e}")
        return None


def process_video_file(input_file, effect, output_dir, verbosity, visualize=False):
    """Process video file by applying audio effects and retaining original bitrate."""

    logger.info(f"Voice : \033[1;95m{effect}\033[0m")
    logger.info(f"Processing video file: {input_file}")

    try:
        # Get the original video bitrate
        original_bitrate = get_bitrate(input_file, verbosity)
        if verbosity and original_bitrate:
            logger.info(
                f"Original video bitrate: \033[33m{original_bitrate}\033[0m")

        # Load the video
        video = VideoFileClip(input_file)
        audio_file = "temp_audio.wav"

        # Extract audio and save it to a file
        if verbosity:
            logger.info("Extract audio and write it to file")
        video.audio.write_audiofile(audio_file)
        audio_segment = AudioSegment.from_file(audio_file)

        # Apply the selected voice effect
        logger.info(f"Apply the [\033[1;90m{effect}\033[0;32m] effect")
        modified_audio = apply_voice_effect(audio_segment, effect)

        # Normalize the modified audio
        modified_audio = normalize_audio(modified_audio)

        # Export the modified audio to a WAV file
        if verbosity:
            logger.info("Export the modified audio to a WAV file")
        modified_audio.export("modified_audio.wav", format="wav")

        # Load the modified audio file back into an AudioFileClip
        new_audio = AudioFileClip("modified_audio.wav")

        # Set the video to use the modified audio
        if verbosity:
            logger.info("Set the video audio to the new modified audio")
        final_video = video.set_audio(new_audio)

        # Define the output file path
        output_file = os.path.join(
            output_dir, f"{effect}_{os.path.basename(input_file)}")

        # Use the original bitrate or default to 5000k if unavailable
        if verbosity:
            logger.info(f"Set:\n\tCodec = [\033[95mlibx264\033[0;32m]\n"
                        f"\tCodec type = [\033[95maac\033[0;32m]\n"
                        f"\tBitrate = [\033[95m{original_bitrate or '5000k'}\033[0m]")

        final_video.write_videofile(
            output_file, codec="libx264", audio_codec="aac", bitrate=original_bitrate or "5000k"
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

    except Exception as e:
        logger.error(f"Error processing video file {input_file}: {e}")
        # raise


def visualize_audio(original_file, modified_file):
    logging.info(f"Visualizing audio: {original_file} and {modified_file}")
    try:
        original_data, original_sr = sf.read(original_file)
        modified_data, modified_sr = sf.read(modified_file)

        plt.figure(figsize=(14, 5))
        plt.subplot(2, 1, 1)
        plt.plot(original_data)
        plt.title("Original Audio Waveform")
        plt.subplot(2, 1, 2)
        plt.plot(modified_data)
        plt.title("Modified Audio Waveform")
        plt.show()

    except Exception as e:
        logger.error(f"Error visualizing audio: {e}")


def transcribe_audio(input_file):
    logger.info(f"Transcribing audio: {input_file}")
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(input_file) as source:
            audio = recognizer.record(source)
        transcription = recognizer.recognize_google(audio)
        logger.info(f"Transcription: {transcription}")
        return transcription
    except Exception as e:
        logger.error(f"Error transcribing audio file {input_file}: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Apply voice effects to audio or video files.")
    parser.add_argument(
        "--input", "-i", help=f"{CYAN}The input audio, video file, or directory.{RESET}")
    parser.add_argument('-e', "--effect", choices=["robotic", "deep", "high", "echo", "reverb", "whisper", "demonic", "chipmunk", "hacker", "lowpass", "distortion"],
                        help=f"{CYAN}The voice effect to apply.{RESET}")
    parser.add_argument(
        "-o", "--output", help=f"{CYAN}Output directory for modified files.{RESET}",)
    parser.add_argument("-v", "--verbose", action="store_true",
                        help=f"{CYAN}Increase output verbosity.{RESET}")
    parser.add_argument("-b", "--batch", action="store_true",
                        help=f"{CYAN}Batch process all files in a directory.{RESET}")
    parser.add_argument("--visualize", action="store_true",
                        help=f"{CYAN}Visualize the audio waveform before and after modification.{RESET}")
    parser.add_argument("--transcribe", action="store_true",
                        help=f"{CYAN}Transcribe the audio content before applying the effect.{RESET}")

    args = parser.parse_args()

    output_dir = os.getcwd() if not args.output else args.output
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.output and not os.path.exists(args.output):
        os.makedirs(args.output)

    mime = magic.Magic(mime=True)
    if args.batch:
        try:
            for root, _, files in os.walk(args.input):
                for file in files:
                    full_path = os.path.join(root, file)
                    file_type = mime.from_file(full_path)
                    print(
                        f"{Fore.GREEN}- INFO -{Fore.RESET} \033[1;94mDetected file type: {file_type}\033[0m")
                    if file_type.startswith("audio"):
                        if args.transcribe:
                            transcribe_audio(full_path)
                        process_audio_file(full_path, args.effect,
                                           output_dir, args.verbose, args.visualize)
                    elif file_type.startswith("video"):
                        process_video_file(full_path, args.effect,
                                           output_dir, args.verbose, args.visualize)
                    else:
                        logger.warning(
                            f"Ignoring unsupported file type: {file}")
        except Exception as e:
            logger.info(e)
    else:
        try:
            file_type = mime.from_file(args.input)
            print(
                f"{Fore.GREEN}- INFO -{Fore.RESET} \033[1;94mDetected file type: {file_type}\033[0m")
            if file_type.startswith("audio"):
                if args.transcribe:
                    transcribe_audio(args.input)
                process_audio_file(args.input, args.effect,
                                   output_dir, args.verbose, args.visualize)
            elif file_type.startswith("video"):
                process_video_file(args.input, args.effect,
                                   output_dir, args.verbose, args.visualize)
            else:
                logger.warning(
                    f"Unsupported file type: {file_type}. Only audio and video files are supported.")
        except Exception as e:
            logger.error(e)


if __name__ == "__main__":
    main()
