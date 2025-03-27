"""A basic/simple file analyzer"""

import sys
import cv2
import numpy as np
from utils.colors import foreground
import ffmpeg

fcl = foreground()
RESET = fcl.RESET


class SA:
    """Video - video object subject for analysis
    return video`s: duration, total_area and frame_count"""

    def __init__(self, video):
        self.video = video

    @staticmethod
    def get_info(input_file):
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

    def SimpleAnalyzer(self):
        """Read the video file/obj
        Increase frame count and accumulate area
        Calculate current frame duration
        Display the resulting frame"""

        try:
            # Read the video file
            cap = cv2.VideoCapture(self.video)
            print(f"{fcl.BYELLOW_FG}Initializing..{RESET}")
            # Initialize variables
            # Frame rate (fps)
            bitrate, aspect_ratio, codec_name, channels, encoder = self.get_info(
                self.video
            )
            frame_count = 0
            total_area = 0
            duration = 0

            print(f"{fcl.DCYAN_FG}Working on it{RESET}")
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
            # print(f"Size {fcl.BGREEN_FG}{size}{RESET}Kb")
            print(f"Channels: {fcl.BGREEN_FG}{channels}{RESET}")
            print(f"Encoder {fcl.BGREEN_FG}{encoder}{RESET}")
            print(f"Bitrate {fcl.BGREEN_FG}{bitrate}{RESET}")
            print(f"Aspect ratio{fcl.BGREEN_FG}{aspect_ratio}{RESET}")
            print(f"Codec name {fcl.BGREEN_FG}{codec_name}{RESET}")
            print(f"Total Frames: {fcl.BGREEN_FG}{frame_count}{RESET}")
            print(
                f"Average Frame Area: {fcl.BGREEN_FG}{total_area / frame_count}{RESET}"
            )
            print(f"Duration: {fcl.BGREEN_FG}{duration:.2f}{RESET} seconds")
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
    vi = SA("/home/skye/Music/Melody in My Mind.mp4")
    SA.get_info("/home/skye/Music/Melody in My Mind.mp4")
    vi.SimpleAnalyzer()
