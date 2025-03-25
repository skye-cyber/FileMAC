import numpy as np
from .logger_init import set_logger
import librosa
from pydub import AudioSegment, effects
from scipy.signal import butter, lfilter


logger = set_logger()


class Modulator:
    def __init__(self):
        pass

    def pitch_shift(self, audio_segment, n_steps):
        # Convert the audio samples to a NumPy array in float32
        samples = np.array(audio_segment.get_array_of_samples(), dtype=np.float32)

        # If the audio is stereo, convert it to mono
        if audio_segment.channels == 2:
            samples = audio_segment.set_channels(1)

        # Convert the samples back to NumPy array and flaoting point
        samples = np.array(audio_segment.get_array_of_samples(), dtype=np.float32)

        # Pitch shift (no need to pass sample_rate separately)
        shifted_samples = librosa.effects.pitch_shift(
            samples, sr=audio_segment.frame_rate, n_steps=n_steps
        )

        # Convert the shifted samples back to int16
        shifted_audio = AudioSegment(
            shifted_samples.astype(np.int16).tobytes(),
            frame_rate=audio_segment.frame_rate,
            sample_width=audio_segment.sample_width,
            channels=audio_segment.channels,
        )

        return shifted_audio

    def hacker(self, audio_segment):
        """Applies a deep, robotic voice effect used for anonymity."""

        # Step 1: Pitch shift down (lower the pitch)
        logger.info("Applying deep pitch shift for hacker voice")
        deep_voice = self.pitch_shift(audio_segment, n_steps=-10)

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
        hacker_voice_effect = (
            effects.low_pass_filter(echo_effect, cutoff=2500) if echo_effect else None
        )
        if hacker_voice_effect is None:
            logger.error("Low pass filter failed")
            return None

        return hacker_voice_effect

    def echo(self, samples, delay=0.2, decay=0.5, sample_rate=44100):
        """Apply echo effect with a specified delay and decay."""
        delay_samples = int(sample_rate * delay)
        echo_signal = np.zeros(len(samples) + delay_samples)

        echo_signal[: len(samples)] = samples
        echo_signal[delay_samples:] += decay * samples  # Delayed echo signal

        return echo_signal[: len(samples)]  # Truncate to original length

    def reverb(self, samples, decay=0.7, delay=0.05, sample_rate=44100):
        try:
            """Apply a reverb effect by adding delayed and attenuated copies of the signal."""
            delay_samples = int(sample_rate * delay)

            # Create a delayed version of the samples and attenuate (apply decay)
            reverb_samples = np.zeros_like(samples)

            if samples.ndim == 2:  # Stereo
                for i in range(delay_samples, len(samples)):
                    reverb_samples[i, 0] = (
                        samples[i, 0] + decay * samples[i - delay_samples, 0]
                    )
                    reverb_samples[i, 1] = (
                        samples[i, 1] + decay * samples[i - delay_samples, 1]
                    )
            else:  # Mono
                for i in range(delay_samples, len(samples)):
                    reverb_samples[i] = samples[i] + decay * samples[i - delay_samples]

            return reverb_samples
        except Exception as e:
            logger.error(e)
            # raise

    def lowpass_filter(self, samples, cutoff=200, sample_rate=44100):
        """
        Apply a low-pass filter to remove frequencies higher than the specified cutoff.

        This function uses a 6th-order Butterworth filter to attenuate frequencies above the
        cutoff frequency, effectively smoothing the audio signal.

        Args:
            samples (numpy.ndarray): The audio samples as a NumPy array.
            cutoff (int, optional): The cutoff frequency in Hz. Defaults to 200.
                                    Typical cutoff values:
                                    - Voice: 1000-2000 Hz
                                    - Music: 5000-8000 Hz
                                    - Hiss/noise removal: 200-500 Hz
            sample_rate (int, optional): The sample rate of the audio in Hz. Defaults to 44100.

        Returns:
            numpy.ndarray: The filtered audio samples as a NumPy array.
        """
        logger.info("Apply a low-pass filter to remove frequencies higher than cutoff")
        nyquist = 0.5 * sample_rate
        normal_cutoff = cutoff / nyquist
        b, a = butter(6, normal_cutoff, btype="low", analog=False)
        filtered_samples = lfilter(b, a, samples)

        return filtered_samples

    def distort(self, samples, gain=20, threshold=0.3):
        """Apply distortion by clipping the waveform."""
        logger.info("Apply distortion by clipping the waveform.")
        samples = samples * gain
        samples = np.clip(samples, -threshold, threshold)  # Clip at threshold
        return samples

    def whisper(self, audio_segment):
        return effects.low_pass_filter(audio_segment, 70).apply_gain(-10)

    def lowpass(self, audio_segment):
        return effects.low_pass_filter(audio_segment, cutoff=2200)

    def normalize(self, audio_segment):
        return effects.normalize(audio_segment)
