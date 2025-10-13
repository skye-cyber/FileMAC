"""
    ///////]    ///    ///  ///////]    (O)    //////]     /////      //////]   /////////
   //     //   ///    ///  //      //  ///  ///     ///   //   /   ///     ///    ///
  /////////   ///    ///  //       /  ///  ///      ///  /////    ///      ///   ///
 //     //   ///    ///  //       /  ///   //      //   //    /   //      //    ///
//     //   //////////  /////// /   ///     ///////    ///////     ///////     ///
Perform audio modifications such as adding voice effect to an audio or video file\n
<b>Operation</b>:
<ul>
<li>->Reverb effect</li>
<li>->Lowpass-reduce noise</li>
<li>->Hackers voice</li>
<li>->High voice effect</li>
<li>->Chpmunk effect</li>
<li>->Apply deep voice effect</li>
<li>->Turn voice to whisper</li>
<li>->distort voice</li>
<li>->Apply demonic voice</li>
<li>->Employ robotic voice</li>
</ul>
"""

from .cli import cli, ArgumentsProcessor
from .utils.logging_utils import LoggingFormatter, colored_logger
from .utils.visualizer import audiowave_visualizer
from .utils.metadata_utils import get_audio_bitrate
from .core.codec import AudioSegmentArrayCodec
from .core.effects import VoiceEffectProcessor
from .core.audio.core import AudioModulator, AudioDenoiser

__version__ = "0.2.0"
__all__ = [
    "cli",
    "ArgumentsProcessor",
    "LoggingFormatter",
    "colored_logger",
    "audiowave_visualizer",
    "get_audio_bitrate",
    "AudioSegmentArrayCodec",
    "VoiceEffectProcessor",
    "AudioModulator",
    "AudioDenoiser",
]
LOGO = """
    ///////]    ///    ///  ///////]    (O)    //////]     /////      //////]   /////////
   //     //   ///    ///  //      //  ///  ///     ///   //   /   ///     ///    ///
  /////////   ///    ///  //       /  ///  ///      ///  /////    ///      ///   ///
 //     //   ///    ///  //       /  ///   //      //   //    /   //      //    ///
//     //   //////////  /////// /   ///     ///////    ///////     ///////     ///
"""
