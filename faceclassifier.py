import cv2

class FaceClassifier:
    def __init__(self):
        # Load the cascade
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def detect_faces(self, frame):
        assert(len(frame.shape)==3)
        # assuming frame is in BGR
        # Convert into grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self.face_cascade.detectMultiScale(gray, 1.1, 4)