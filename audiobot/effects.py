from pydub import effects
from .codec import AudioSegmentArrayCodec
from .modulator import Modulator
from .logger_init import set_logger
from pydub import AudioSegment

logger = set_logger()


class Voice:
    def __init__(self, audio_segment, effect: str, verbosity: bool = False):
        self.effect = effect
        self.audio_segment = audio_segment
        self.verbosity = verbosity

    def apply_effect(self):
        handler = AudioSegmentArrayCodec()

        # OK 1.2
        if self.effect == "robotic":
            return Modulator().pitch_shift(
                effects.speedup(self.audio_segment, 1.01), n_steps=-10
            )

        # OK
        elif self.effect == "deep":
            return Modulator().pitch_shift(self.audio_segment, n_steps=-4)

        # OK
        elif self.effect == "high":
            return Modulator().pitch_shift(self.audio_segment, n_steps=4)

        # OK
        elif self.effect == "chipmunk":
            return Modulator().pitch_shift(
                effects.speedup(self.audio_segment, 1.01), n_steps=9
            )

        elif self.effect == "demonic":
            return (
                Modulator()
                .pitch_shift(effects.speedup(self.audio_segment, 1.01), n_steps=-10)
                .overlay(
                    AudioSegment.silent(duration=700) + self.audio_segment.fade_out(500)
                )
            )
            # return seg.overlay(pitch_shift(effects.speedup(self.audio_segment, 1.01),\n
            # n_steps=11).overlay(AudioSegment.silent(duration=250) + self.audio_segment.fade_out(2000)))

        # OK
        elif self.effect == "echo":
            delay = AudioSegment.silent(duration=1000)  # 1000ms of silence
            return self.audio_segment.overlay(delay + self.audio_segment)

        # OK
        elif self.effect == "reverb":
            # Convert to numpy array

            samples, sample_rate = handler.audiosegment_to_numpy(self.audio_segment)

            # Apply the reverb effect
            samples = Modulator().reverb(samples)

            # Convert back to AudioSegment
            processed_audio = handler.numpy_to_audiosegment(
                samples,
                sample_rate,
                self.audio_segment.sample_width,
                self.audio_segment.channels,
            )

            return processed_audio
            # Simple reverb effect
            # delay = AudioSegment.silent(duration=150)  # 150ms of silence
            # return self.audio_segment.overlay(delay + self.audio_segment.fade_out(3000))

        elif self.effect == "whisper":
            return Modulator().whisper(self.audio_segment)

        # OK
        elif self.effect == "hacker":
            return Modulator().hacker(self.audio_segment)

        elif self.effect == "distortion":
            # Convert to numpy array
            samples, sample_rate = handler.audiosegment_to_numpy(self.audio_segment)

            # Apply the distortion effect
            samples = Modulator().distort(samples)

            # Convert back to AudioSegment
            processed_audio = handler.numpy_to_audiosegment(
                samples,
                sample_rate,
                self.audio_segment.sample_width,
                self.audio_segment.channels,
            )

            return processed_audio

        # OK
        elif self.effect == "lowpass":
            # processed_audio
            return Modulator().lowpass(self.audio_segment)

        else:
            if self.verbosity:
                logger.critical(f"Unknown voice effect: {self.effect}")


def _get_effects_() -> list:
    """
    This function returns supported voice effects
    Args:
        None
    Returns:
        list
    """
    effects = [
        "robotic",
        "deep",
        "high",
        "echo",
        "reverb",
        "whisper",
        "demonic",
        "chipmunk",
        "hacker",
        "lowpass",
        "distortion",
    ]
    return effects
