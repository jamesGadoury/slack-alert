import cv2
import argparse

def main(args):
    # define a video capture object
    videoCapture = cv2.VideoCapture(0)

    # Load the cascade
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    windowName = 'VideoCapture'
    windowWidth = 1280
    windowHeight = 720

    multipleFacesDetectedCount = 0

    while(True):
        # Capture the video frame by frame
        ret, frame = videoCapture.read()

        cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(windowName, windowWidth, windowHeight)

        # Convert into grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = faceCascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) > 1:
            multipleFacesDetectedCount += 1

        if multipleFacesDetectedCount == args.frames:
            print("Multiple faces detected for a while!")
            multipleFacesDetectedCount = 0

        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Display the resulting frame
        cv2.imshow(windowName, frame)

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