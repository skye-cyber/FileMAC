#!/usr/bin/python3
import numpy as np
import sounddevice as sd
import wavio
import time
from pynput import keyboard

fs = 44100  # Sample rate (samples per second)
channels = 2  # Number of audio channels
dtype = np.int16  # Data type for the recording

paused = False  # Global flag for pause
recording = []  # Buffer for recorded chunks
start_time = 0  # Start time for elapsed time tracking
elapsed_time = 0  # Track elapsed time
running = True  # Track recording status


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    sec = int(seconds % 60)
    return f"\033[34m{hours:02d}\033[35m:{minutes:02d}\033[32m:{sec:02d}\033[0m"


def on_press(key):
    global paused, running
    try:
        if key == keyboard.Key.space:
            paused = not paused  # Toggle pause/resume
            if paused:
                print("\nPaused... Press SPACE to resume.")
            else:
                print("\nRecording resumed... Press SPACE to pause.")
        elif key == keyboard.Key.enter:
            running = False  # Stop recording
            print("\nRecording finished.")
            return False  # Stop listener
    except Exception as e:
        print(f"Error: {e}")


def record_audio():
    global paused, recording, start_time, elapsed_time, running
    print("Press SPACE to pause/resume, ENTER to stop and save.")
    start_time = time.time()

    def callback(indata, frames, callback_time, status):
        if not paused:
            recording.append(indata.copy())
            elapsed_time = time.time() - start_time
        print(f"Elapsed Time: {format_time(elapsed_time)}", end="\r")

    with sd.InputStream(
        samplerate=fs, channels=channels, dtype=dtype, callback=callback
    ):
        with keyboard.Listener(on_press=on_press) as listener:
            while running:
                time.sleep(0.1)  # Prevents high CPU usage
            listener.stop()

    return np.concatenate(recording, axis=0) if recording else np.array([], dtype=dtype)


def save_audio(filename, recording, fs):
    if recording.size == 0:
        print("No audio recorded.")
    else:
        wavio.write(filename, recording, fs, sampwidth=2)
        print(f"Recording saved as {filename}")


if __name__ == "__main__":
    try:
        filename = input("\033[94mEnter Desired File Name\033[0;1;89m:") + ".wav"
        recorded_data = record_audio()
        save_audio(filename, recorded_data, fs)
    except KeyboardInterrupt:
        print("\nQuit!")
        exit(1)
