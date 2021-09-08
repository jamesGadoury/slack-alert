import cv2
import argparse
from video import VideoCaptureWindow
from frameprocessing import ConditionalFrameEvaluator, MultipleFaceChecker, FrameDebugger

def main(args):
    # define a video capture object
    video_capture = cv2.VideoCapture(0)

    window = VideoCaptureWindow()

    conditional_evaluator = ConditionalFrameEvaluator(MultipleFaceChecker(), args.frames)

    debugger = FrameDebugger() if args.debug else None

    while(True):
        # Capture the video frame by frame
        ret, frame = video_capture.read()

        window.generate()

        if conditional_evaluator.evaluate(frame):
            print("Multiple faces detected for a while!")

        if debugger:
            debugger.debug(frame)

        # Display the resulting frame
        window.update_frame(frame)

        if window.exit_event():
            break

    # Release the video capture object
    video_capture.release()

    # Destroy the video capture window
    window.destroy()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('frames', type=int, help='number of frames that satisfies a condition before sending slack message')
    parser.add_argument('--debug', action='store_true', help='flag turns on debug logic')
    main(parser.parse_args())