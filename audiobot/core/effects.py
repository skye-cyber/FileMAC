from pydub import effects
from .codec import AudioSegmentArrayCodec
from .audio.core import AudioModulator
from ..utils.logging_utils import colored_logger
from pydub import AudioSegment

# logger = colored_logger()


class VoiceEffectProcessor:
    def __init__(self, audio_segment, effect: str, verbosity: bool = False):
        self.effect = effect.lower()
        self.audio_segment = audio_segment
        self.verbosity = verbosity
        self.handler = AudioSegmentArrayCodec()
        self.logger = colored_logger()

    def _apply_chipmunk(self):
        return AudioModulator().pitch_shift(
            effects.speedup(self.audio_segment, 1.01), n_steps=9
        )

    def _apply_high(self):
        return AudioModulator().pitch_shift(self.audio_segment, n_steps=4)

    def _apply_lowpass(self):
        return AudioModulator().lowpass(self.audio_segment)

    def _apply_highpass(self):
        return AudioModulator().highpass(self.audio_segment)

    def _apply_robotic(self):
        return AudioModulator().pitch_shift(
            effects.speedup(self.audio_segment, 1.01), n_steps=-10
        )

    def _apply_demonic(self):
        return (
            AudioModulator()
            .pitch_shift(effects.speedup(self.audio_segment, 1.01), n_steps=-10)
            .overlay(
                AudioSegment.silent(duration=700) + self.audio_segment.fade_out(500)
            )
        )

    def _apply_hacker(self):
        return AudioModulator().hacker(self.audio_segment)

    def _apply_distortion(self):
        samples, sample_rate = self.handler.audiosegment_to_numpy(self.audio_segment)
        distorted_samples = AudioModulator().distort(samples)
        return self.handler.numpy_to_audiosegment(
            distorted_samples,
            sample_rate,
            self.audio_segment.sample_width,
            self.audio_segment.channels,
        )

    def _apply_deep(self):
        return AudioModulator().pitch_shift(self.audio_segment, n_steps=-4)

    def _apply_echo(self):
        delay = AudioSegment.silent(duration=1000)
        return self.audio_segment.overlay(delay + self.audio_segment)

    def _apply_whisper(self):
        return AudioModulator().whisper(self.audio_segment)

    def _apply_reverb(self):
        samples, sample_rate = self.handler.audiosegment_to_numpy(self.audio_segment)
        reverbed_samples = AudioModulator().reverb(samples)
        return self.handler.numpy_to_audiosegment(
            reverbed_samples,
            sample_rate,
            self.audio_segment.sample_width,
            self.audio_segment.channels,
        )

    def denoise(self):
        from .modulator import AudioDenoiser

        sample, sample_rate = self.handler.audiosegment_to_numpy(self.audio_segment)
        denoised_sample = AudioDenoiser().denoise(sample)
        audio_segment = self.handler.numpy_to_audiosegment(
            denoised_sample,
            sample_rate,
            self.audio_segment.sample_width,
            self.audio_segment.channels,
        )
        return audio_segment

    def _get_effects(self):
        return {
            "chipmunk": self._apply_chipmunk,
            "high": self._apply_high,
            "lowpass": self._apply_lowpass,
            "robotic": self._apply_robotic,
            "demonic": self._apply_demonic,
            "hacker": self._apply_hacker,
            "distortion": self._apply_distortion,
            "deep": self._apply_deep,
            "echo": self._apply_echo,
            "whisper": self._apply_whisper,
            "reverb": self._apply_reverb,
            "denoise": self.denoise,
            "highpass": self._apply_highpass,
        }

    def apply_effect(self):
        effect_handler = self._get_effects().get(self.effect)
        if effect_handler:
            return effect_handler()
        elif self.verbosity:
            self.logger.critical(f"Unknown voice effect: {self.effect}")
            return self.audio_segment  # Return unmodified audio if effect is unknown
