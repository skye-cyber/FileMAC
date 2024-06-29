import sys
import cv2
import numpy as np
from .colors import DYELLOW, RESET, DCYAN, DGREEN


class SA:

    def __init__(self, video):
        self.video = video

    def SimpleAnalyzer(self):
        try:
            # Read the video file
            cap = cv2.VideoCapture(self.video)
            print(f"{DYELLOW}Initializing..{RESET}")
            # Initialize variables
            frame_count = 0
            total_area = 0
            duration = 0

            print(f"{DCYAN}mWorking on it{RESET}")
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
                cv2.imshow('Frame', frame)

                # Break the loop after pressing 'q'
                if cv2.waitKey(1) == ord('q'):
                    break

            # Release the video capture object and close all windows
            cap.release()
            cv2.destroyAllWindows()

            # Print results
            print(f"Total Frames: {DGREEN}{frame_count}{RESET}")
            print(f"Average Frame Area: {DGREEN}{total_area / frame_count}{RESET}")
            print(f"Duration: {DGREEN}{duration}{RESET} seconds")
        except KeyboardInterrupt:
            print("\nExiting")
            sys.exit(1)
        except Exception as e:
            print(e)
            sys.exit(1)


if __name__ == "__main__":
    vi = SA("/home/skye/Music/Melody in My Mind.mp4")
    vi.SimpleAnalyzer()
