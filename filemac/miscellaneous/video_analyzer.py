"""A basic/simple file analyzer"""

import sys
import cv2
import numpy as np
from ..utils.colors import fg, rs
import ffmpeg

RESET = rs


class SimpleAnalyzer:
    """Video - video object subject for analysis
    return video`s: duration, total_area and frame_count"""

    def __init__(self, video):
        self.video = video

    @staticmethod
    def get_metadata(input_file):
        """Fetch the original bitrate of the video file using ffmpeg."""
        try:
            probe = ffmpeg.probe(input_file)
            print(probe.get("streams")[1])
            bitrate = None
            # Iterate over the streams and find the video stream
            for stream in probe["streams"]:
                bitrate = (
                    stream.get("bit_rate", None)
                    if stream["codec_type"] == "video"
                    else None
                )
                aspect_ratio = (
                    stream.get("sample_aspect_ratio")
                    if stream["sample_aspect_ratio"]
                    else None
                )
                codec_name = stream.get("codec_name") if stream["codec_name"] else None
                channels = stream.get("channels")

                encoder = stream.get("encoder") if stream.get("encoder") else None
                break
            return bitrate, aspect_ratio, codec_name, channels, encoder
        except ffmpeg.Error as e:
            raise
            print(f"Error: {e}")
        except Exception as e:
            raise
            print(f"Error: {e}")

    def analyze(self):
        """Read the video file/obj
        Increase frame count and accumulate area
        Calculate current frame duration
        Display the resulting frame"""

        try:
            # Read the video file
            cap = cv2.VideoCapture(self.video)
            print(f"{fg.BYELLOW}Initializing..{RESET}")
            # Initialize variables
            # Frame rate (fps)
            bitrate, aspect_ratio, codec_name, channels, encoder = self.get_metadata(
                self.video
            )
            frame_count = 0
            total_area = 0
            duration = 0

            print(f"{fg.DCYAN}Working on it{RESET}")
            while True:
                ret, frame = cap.read()

                if not ret:
                    break
                # Increase frame count and accumulate area
                frame_count += 1
                total_area += np.prod(frame.shape[:2])

                # Calculate current frame duration
                fps = cap.get(cv2.CAP_PROP_FPS)
                duration += 1 / fps

                # Display the resulting frame
                cv2.imshow("Frame", frame)

                # Break the loop after pressing 'q'
                if cv2.waitKey(1) == ord("q"):
                    break

            # Release the video capture object and close all windows
            cap.release()
            cv2.destroyAllWindows()

            # Print results
            # print(f"Size {fg.BGREEN}{size}{RESET}Kb")
            print(f"Channels: {fg.BGREEN}{channels}{RESET}")
            print(f"Encoder {fg.BGREEN}{encoder}{RESET}")
            print(f"Bitrate {fg.BGREEN}{bitrate}{RESET}")
            print(f"Aspect ratio{fg.BGREEN}{aspect_ratio}{RESET}")
            print(f"Codec name {fg.BGREEN}{codec_name}{RESET}")
            print(f"Total Frames: {fg.BGREEN}{frame_count}{RESET}")
            print(
                f"Average Frame Area: {fg.BGREEN}{total_area / frame_count}{RESET}"
            )
            print(f"Duration: {fg.BGREEN}{duration:.2f}{RESET} seconds")
            return frame_count, total_area, duration
        except KeyboardInterrupt:
            print("\nExiting")
            sys.exit(1)
        except TypeError:
            pass
        except Exception as e:
            print(e)
            sys.exit(1)


if __name__ == "__main__":
    vi = SimpleAnalyzer("/home/skye/Videos/demo.mkv")
    # SimpleAnalyzer.get_metadata("/home/skye/Videos/demo.mkv")
    vi.analyze()
