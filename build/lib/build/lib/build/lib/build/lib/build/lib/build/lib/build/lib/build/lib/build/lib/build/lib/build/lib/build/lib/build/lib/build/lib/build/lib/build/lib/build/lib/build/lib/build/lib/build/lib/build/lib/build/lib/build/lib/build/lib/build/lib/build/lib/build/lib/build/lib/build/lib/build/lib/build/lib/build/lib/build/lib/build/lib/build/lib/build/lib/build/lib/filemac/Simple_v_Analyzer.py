import sys
import cv2
import numpy as np


class SA:

    def __init__(self, video):
        self.video = video

    def SimpleAnalyzer(self):
        try:
            # Read the video file
            cap = cv2.VideoCapture(self.video)
            print("\033[1;33mInitializing..\033[0m")
            # Initialize variables
            frame_count = 0
            total_area = 0
            duration = 0

            print("\033[1;36mWorking on it")
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
            print(f"Total Frames: \033[1;32m{frame_count}\033[0m")
            print(f"Average Frame Area: \033[1;32m{total_area / frame_count}\033[0m")
            print(f"Duration: \033[1;32m{duration}\033[0m seconds")
        except KeyboardInterrupt:
            print("\nExiting")
            sys.exit(1)
        except Exception as e:
            print(e)
            sys.exit(1)


if __name__ == "__main__":
    vi = SA("/home/skye/Music/Melody in My Mind.mp4")
    vi.SimpleAnalyzer()
