from pydub import AudioSegment
import numpy as np


class AudioSegmentArrayCodec:
    """
    This class provides functionality to convert between pydub AudioSegments and NumPy arrays.

    It allows for the following conversions:\n
        1. AudioSegments to NumPy arrays.
        2. NumPy arrays to AudioSegments.
    """

    def __init__(self):
        """
        Initializes the AudioSegmentArrayCodec object.
        Currently, this constructor does not perform any specific operations.
        """
        self = self  # Note: This line has no effect and can be removed.

    def numpy_to_audiosegment(self, samples, sample_rate, sample_width, channels):
        """
        Converts a NumPy array to a pydub AudioSegment.

        Args:
            samples (numpy.ndarray): The NumPy array representing the audio samples.
            sample_rate (int): The sample rate of the audio in Hz.
            sample_width (int): The sample width in bytes (e.g., 2 for 16-bit audio).
            channels (int): The number of audio channels (1 for mono, 2 for stereo).

        Returns:
            pydub.AudioSegment: An AudioSegment object created from the NumPy array.
        """
        # Flatten the array if it has 2 channels (stereo)
        if len(samples.shape) == 2 and channels == 2:
            samples = samples.flatten()

        # Convert the NumPy array to raw audio data
        raw_data = samples.tobytes()

        # Create a new AudioSegment using the raw audio data
        return AudioSegment(
            data=raw_data,
            sample_width=sample_width,
            frame_rate=sample_rate,
            channels=channels,
        )

    def audiosegment_to_numpy(self, audio_segment):
        """
        Converts a pydub AudioSegment to a NumPy array.

        Args:
            audio_segment (pydub.AudioSegment): The AudioSegment object to convert.

        Returns:
            tuple: A tuple containing:
                - numpy.ndarray: The NumPy array representing the audio samples.
                - int: The sample rate of the audio in Hz.
        """
        samples = np.array(audio_segment.get_array_of_samples())

        # If stereo, reshape to (n_samples, 2)
        if audio_segment.channels == 2:
            samples = samples.reshape((-1, 2))

        return samples, audio_segment.frame_rate
