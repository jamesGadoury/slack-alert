import cv2
import argparse


WINDOW_NAME = 'VideoCapture'
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

def generate_window():
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, WINDOW_WIDTH, WINDOW_HEIGHT)

class FaceClassifier:
    def __init__(self):
        # Load the cascade
        self.faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def detect_faces(self, frame):
        assert(len(frame.shape)==3)
        # assuming frame is in BGR
        # Convert into grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self.faceCascade.detectMultiScale(gray, 1.1, 4)

def main(args):
    # define a video capture object
    videoCapture = cv2.VideoCapture(0)

    faceClassifier = FaceClassifier()

    multipleFacesDetectedCount = 0

    while(True):
        # Capture the video frame by frame
        ret, frame = videoCapture.read()

        generate_window()

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
        cv2.imshow(WINDOW_NAME, frame)

        # the 'q' button is set as the quitting button
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object
    videoCapture.release()

    # Destroy all the windows
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--frames', type=int, help='number of frames that satisfies a condition before sending slack message')
    main(parser.parse_args())