import cv2
import argparse
from video import VideoCaptureWindow
from faceclassifier import FaceClassifier

class ConditionalFrameEvaluator:
    def __init__(self, condition_checker, threshold):
        self.condition_checker = condition_checker
        self.threshold = threshold
        self.counter = 0

    def evaluate(self, frame):
        if self.condition_checker.check(frame):
            self.counter += 1
        if self.counter == self.threshold:
            self.counter = 0
            return True
        return False


class MultipleFaceChecker:
    def __init__(self):
        self.face_classifier = FaceClassifier()

    def check(self, frame):
        # Detect faces
        faces = self.face_classifier.detect_faces(frame)
        return len(faces) > 1

def mutate_frame_with_face_rectangles(frame):
    face_classifier = FaceClassifier()
    faces = face_classifier.detect_faces(frame)
    # Draw rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

def main(args):
    # define a video capture object
    video_capture = cv2.VideoCapture(0)

    window = VideoCaptureWindow()

    conditional_evaluator = ConditionalFrameEvaluator(MultipleFaceChecker(), args.frames)

    while(True):
        # Capture the video frame by frame
        ret, frame = video_capture.read()

        window.generate()

        if conditional_evaluator.evaluate(frame):
            print("Multiple faces detected for a while!")

        if args.debug:
            mutate_frame_with_face_rectangles(frame)

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
    parser.add_argument('--frames', type=int, help='number of frames that satisfies a condition before sending slack message')
    parser.add_argument('--debug', action='store_true', help='flag turns on debug logic')
    main(parser.parse_args())