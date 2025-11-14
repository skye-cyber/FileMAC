#!/usr/bin/python3
import numpy as np
import sounddevice as sd
import wavio
import time
from pynput import keyboard
import sys


class SoundRecorder:
    def __init__(self, frequency=44100, channels=2, dtype=np.int16):
        self.fs = frequency  # Sample rate (samples per second)
        self.channels = 2  # Number of audio channels
        self.dtype = dtype  # Data type for the recording

        self.paused = False  # Global flag for pause
        self.recording = []  # Buffer for recorded chunks
        self.start_time = 0  # Start time for elapsed time tracking
        self.elapsed_time = 0  # Track elapsed time
        self.running = True  # Track recording status
        self.filename = self.filename_prober()

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        sec = int(seconds % 60)
        return f"\033[34m{hours:02d}\033[35m:{minutes:02d}\033[32m:{sec:02d} \033[0m"

    def on_press(self, key):
        # global paused, running
        try:
            if key == keyboard.Key.space:
                self.paused = not self.paused  # Toggle pause/resume
                if self.paused:
                    print("\nPaused... Press SPACE to resume.")
                else:
                    print("\nRecording resumed... Press SPACE to pause.")
            elif key == keyboard.Key.enter:
                self.running = False  # Stop recording
                print("\nRecording finished.")
                return False  # Stop listener
        except Exception as e:
            print(f"Error: {e}")

    def record_audio(self):
        # global paused, recording, start_time, elapsed_time, running
        print("Press SPACE to pause/resume, ENTER to stop and save.")
        start_time = time.time()

        def callback(indata, frames, callback_time, status):
            if not self.paused:
                self.recording.append(indata.copy())
                self.elapsed_time = time.time() - start_time
            print(f"Elapsed Time: {self.format_time(self.elapsed_time)}", end="\r")

        with sd.InputStream(
            samplerate=self.fs,
            channels=self.channels,
            dtype=self.dtype,
            callback=callback,
        ):
            with keyboard.Listener(on_press=self.on_press) as listener:
                while self.running:
                    time.sleep(0.1)  # Prevents high CPU usage
                listener.stop()

        return (
            np.concatenate(self.recording, axis=0)
            if self.recording
            else np.array([], dtype=self.dtype)
        )

    def run(self):
        try:
            r_data = self.record_audio()
            self.save_audio(r_data)
            return self.filename
        except KeyboardInterrupt:
            sys.exit()

    def save_audio(self, recording):
        if recording.size == 0:
            print("No audio recorded.")
        else:
            wavio.write(self.filename, recording, self.fs, sampwidth=2)
            print(f"Recording saved as {self.filename}")

    @staticmethod
    def filename_prober():
        _filename = None

        while not _filename:
            _filename = input("\033[94mEnter Desired File Name\033[0;1;89m:")

        filename = f"{_filename}.wav" if len(_filename.split(".")) < 2 else _filename
        return filename


if __name__ == "__main__":
    try:
        filename = input("\033[94mEnter Desired File Name\033[0;1;89m:") + ".wav"
        recorder = SoundRecorder()
        file = recorder.run()
    except KeyboardInterrupt:
        print("\nQuit!")
        exit(1)
