import cv2
import argparse
from video import VideoCaptureWindow
from faceclassifier import FaceClassifier

def main(args):
    # define a video capture object
    video_capture = cv2.VideoCapture(0)

    window = VideoCaptureWindow()

    face_classifier = FaceClassifier()

    multiple_faces_detected_count = 0

    while(True):
        # Capture the video frame by frame
        ret, frame = video_capture.read()

        window.generate()

        # Detect faces
        faces = face_classifier.detect_faces(frame)

        if len(faces) > 1:
            multiple_faces_detected_count += 1

        if multiple_faces_detected_count == args.frames:
            print("Multiple faces detected for a while!")
            multiple_faces_detected_count = 0

        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

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
    main(parser.parse_args())