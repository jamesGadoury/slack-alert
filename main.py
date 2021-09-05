import cv2
import argparse
from video import VideoCaptureWindow
from faceclassifier import FaceClassifier

def main(args):
    # define a video capture object
    videoCapture = cv2.VideoCapture(0)

    window = VideoCaptureWindow()

    faceClassifier = FaceClassifier()

    multipleFacesDetectedCount = 0

    while(True):
        # Capture the video frame by frame
        ret, frame = videoCapture.read()

        window.generate()

        # Detect faces
        faces = faceClassifier.detect_faces(frame)

        if len(faces) > 1:
            multipleFacesDetectedCount += 1

        if multipleFacesDetectedCount == args.frames:
            print("Multiple faces detected for a while!")
            multipleFacesDetectedCount = 0

        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Display the resulting frame
        window.updateFrame(frame)

        # the 'q' button is set as the quitting button
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object
    videoCapture.release()

    # Destroy the video capture window
    window.destroy()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--frames', type=int, help='number of frames that satisfies a condition before sending slack message')
    main(parser.parse_args())