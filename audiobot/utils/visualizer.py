import matplotlib.pyplot as plt
import soundfile as sf
from .logging_utils import colored_logger


Clogger = colored_logger()


def audiowave_visualizer(original_file, modified_file):
    Clogger.info(f"Visualizing audio: {original_file} and {modified_file}")
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
        Clogger.error(f"Error visualizing audio: {e}")
