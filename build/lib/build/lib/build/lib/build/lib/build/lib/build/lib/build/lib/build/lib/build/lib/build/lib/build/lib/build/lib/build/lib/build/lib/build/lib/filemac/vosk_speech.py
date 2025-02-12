import json
import os
import shutil

import pyaudio
from vosk import KaldiRecognizer, Model

# Constants
MODEL_PATH = "../src/vosk-model-en-us-0.22-lgraph"
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
FRAMES_PER_BUFFER = 8000


def wrap_text(text, width):
    """Wrap the text to fit within the specified width."""
    import textwrap
    return "\n".join(textwrap.wrap(text, width))


def print_text(wrapped_text, prompt_message, color_code):
    """Clear the screen and print the wrapped text with a prompt message."""
    os.system("clear")  # Clear the screen
    print(prompt_message)
    print(f"\033[{color_code}m{wrapped_text}\033[0m", end='\r')


def main():
    # Load the Vosk model
    try:
        model = Model(MODEL_PATH)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    recognizer = KaldiRecognizer(model, RATE)

    # Set up the audio stream
    audio = pyaudio.PyAudio()
    try:
        stream = audio.open(format=AUDIO_FORMAT, channels=CHANNELS,
                            rate=RATE, input=True, frames_per_buffer=FRAMES_PER_BUFFER)
        stream.start_stream()
    except Exception as e:
        print(f"Error opening audio stream: {e}")
        return

    print("\033[1;30mSpeak into the microphone...\033[0m")
    text = ""
    terminal_width = shutil.get_terminal_size().columns

    try:
        while True:
            data = stream.read(FRAMES_PER_BUFFER)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text += " " + result['text']
                wrapped_text = wrap_text(text.strip(), terminal_width)
                print_text(
                    wrapped_text, "\033[1;30mSpeak into the microphone...\033[0m", "32")
            else:
                partial_result = json.loads(recognizer.PartialResult())
                partial_text = partial_result['partial']
                wrapped_partial = wrap_text(
                    text.strip() + " " + partial_text, terminal_width)
                print_text(
                    wrapped_partial, "\033[1;30mSpeak into the microphone...\033[0m", "36")

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


if __name__ == "__main__":
    main()
