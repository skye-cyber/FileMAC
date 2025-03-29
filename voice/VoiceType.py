#!/usr/bin/env python
import sys
import logging
import threading
import speech_recognition as sr
import pyautogui
import subprocess  # For Linux typing fallback
from queue import Queue
from threading import Event, Lock
from pynput import keyboard  # Replaces `keyboard` for hotkeys

# Configuration
CONFIG = {
    "hotkey_listen": "<ctrl>+<alt>+v",
    "hotkey_exit": "<esc>",
    "energy_threshold": 300,
    "pause_threshold": 0.8,
    "timeout_listen": 5,
    "lang": "en-US",
    "fallback_clipboard": True,
    "log_file": "voicetype.log",
}


class VoiceTypeEngine:
    def __init__(self):
        self.r = sr.Recognizer()
        self.audio_queue = Queue()
        self.is_listening = Event()
        self.lock = Lock()
        self.setup_logging()
        self.configure_recognizer()
        self.auto_select_microphone()  # Auto-detect microphone

    def setup_logging(self):
        logging.basicConfig(
            filename=CONFIG["log_file"],
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    def configure_recognizer(self):
        self.r.energy_threshold = CONFIG["energy_threshold"]
        self.r.dynamic_energy_threshold = False
        self.r.pause_threshold = CONFIG["pause_threshold"]

    def safe_type_text(self, text):
        """Types text using GUI automation, avoiding root requirements."""
        try:
            with self.lock:
                if sys.platform == "linux":
                    # Linux alternative
                    subprocess.run(["xdotool", "type", text + " "])
                else:
                    pyautogui.write(text + " ")
        except Exception as e:
            logging.error("Typing failed: %s", e)
            print(f"Typing failed: {e}")
            if CONFIG["fallback_clipboard"]:
                self.clipboard_fallback(text)

    def clipboard_fallback(self, text):
        """Fallback method using clipboard if typing fails."""
        try:
            import pyperclip

            pyperclip.copy(text)
            pyautogui.hotkey("ctrl", "v")
        except Exception as e:
            logging.error("Clipboard fallback failed: %s", e)

    def process_audio(self):
        """Processes recognized speech and converts it to text."""
        while self.is_listening.is_set() or not self.audio_queue.empty():
            try:
                audio_data = self.audio_queue.get(timeout=1)
                text = self.r.recognize_google(audio_data, language=CONFIG["lang"])
                logging.info("Recognized: %s", text)
                print(f"Recognized: {text}")
                self.safe_type_text(text)
            except sr.UnknownValueError:
                logging.warning("Speech not recognized")
            except sr.RequestError as e:
                logging.error("API unreachable: %s", e)
            except Exception as e:
                logging.error("Unexpected error: %s", e)

    def listen_worker(self):
        """Listens for speech input and sends it to processing queue."""
        with sr.Microphone(device_index=self.microphone_index) as source:
            while self.is_listening.is_set():
                try:
                    audio = self.r.listen(
                        source, timeout=CONFIG["timeout_listen"], phrase_time_limit=10
                    )
                    self.audio_queue.put(audio)
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    logging.error("Recording error: %s", e)

    def auto_select_microphone(self):
        """Automatically selects the default microphone."""
        try:
            with sr.Microphone() as source:
                print(f"Using default microphone: {source}")
                self.microphone_index = None  # Auto-select default mic
        except Exception as e:
            logging.error("Microphone access error: %s", e)
            sys.exit("Error: Unable to access microphone")

    def start(self):
        """Starts the VoiceType engine with hotkey support."""
        logging.info("VoiceType Pro Started")
        print(
            f"VoiceType Pro Active\nStart typing: {CONFIG['hotkey_listen']}\nExit: {CONFIG['hotkey_exit']}"
        )

        listener = keyboard.GlobalHotKeys(
            {
                CONFIG["hotkey_listen"]: self.toggle_listening,
                CONFIG["hotkey_exit"]: self.shutdown,
            }
        )

        listener.start()
        listener.join()  # Keep listening for hotkeys

    def toggle_listening(self):
        """Toggles the voice listening state."""
        if not self.is_listening.is_set():
            self.is_listening.set()
            threading.Thread(target=self.listen_worker, daemon=True).start()
            threading.Thread(target=self.process_audio, daemon=True).start()
        else:
            self.is_listening.clear()

    def shutdown(self):
        """Gracefully shuts down the program."""
        self.is_listening.clear()
        logging.info("VoiceType Pro Shutdown")
        print("\nVoiceType Pro terminated")
        sys.exit(0)


if __name__ == "__main__":
    try:
        engine = VoiceTypeEngine()
        engine.start()
    except Exception as e:
        logging.critical("Critical failure: %s", e)
        print(f"Critical error: {str(e)}")
        sys.exit(1)
