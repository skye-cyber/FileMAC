#!/usr/bin/python3
import keyboard
import numpy as np
import sounddevice as sd
import wavio

fs = 44100  # Sample rate (samples per second)
channels = 2  # Number of audio channels
dtype = np.int16  # Data type for the recording


def record_audio():
    print("Press SPACE to pause/resume, ENTER to stop and save.")
    recording = []
    paused = False

    # Buffer for recording chunks
    def callback(indata, frames, time, status):
        if not paused:
            recording.append(indata.copy())

    # Start stream for recording
    with sd.InputStream(samplerate=fs, channels=channels, dtype=dtype, callback=callback):
        while True:
            if keyboard.is_pressed("space"):
                paused = not paused  # Toggle pause/resume
                if paused:
                    print("Paused... Press SPACE to resume.")
                else:
                    print("Recording resumed... Press SPACE to pause.")

                # Wait until the key is released to avoid multiple triggers
                while keyboard.is_pressed("space"):
                    pass

            if keyboard.is_pressed("enter"):
                print("Recording finished.")
                break

    # Concatenate the chunks of data recorded
    recording = np.concatenate(recording, axis=0)
    return recording


def save_audio(filename, recording, fs):
    wavio.write(filename, recording, fs, sampwidth=2)
    print(f"Recording saved as {filename}")


if __name__ == "__main__":
    try:
        filename = input("\033[94mEnter Desired File Name\033[0;1;89m:") + str('.wav')
        recording = record_audio()
        save_audio(filename, recording, fs)
    except KeyboardInterrupt:
        print("\nQuit!")
        exit(1)
