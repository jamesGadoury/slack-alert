import cv2
from face_recognition.api import face_encodings, face_locations
from faceclassifier import FaceClassifier
import face_recognition

class ConditionalFrameEvaluator:
    def __init__(self, condition_checker, threshold):
        self.condition_checker = condition_checker
        self.threshold = threshold
        self.counter = 0

    def evaluate(self, frame):
        if self.condition_checker.check(frame):
            self.counter += 1
        elif self.counter > 0:
            # if the counter is non zero, but the condition hasn't been found
            # in this frame, clear the counter
            self.counter = 0
        if self.counter == self.threshold:
            self.counter = 0
            return True
        return False

    def alert(self):
        return self.condition_checker.alert()

class MultipleFaceChecker:
    def __init__(self):
        self.face_classifier = FaceClassifier()

    def check(self, frame):
        # Detect faces
        faces = self.face_classifier.detect_faces(frame)
        return len(faces) > 1

    def alert(self):
        return 'Multiple faces detected!'

def reduce_frame(frame):
    # Resize frame of video to 1/4 size for faster face recognition processing
    return cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

def convert_to_rgb(frame):
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    return frame[:, :, ::-1]

class NotYourFaceChecker:
    def __init__(self, your_image_file):
        your_image = face_recognition.load_image_file(your_image_file)
        self.known_face_encodings = [ face_recognition.face_encodings(your_image)[0] ]
    
    def check(self, frame):
        frame = reduce_frame(convert_to_rgb(frame))

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)

            if False in matches:
                return True

        return False

    def alert(self):
        return 'A face that wasn\'t yours was detected!'

class FrameDebugger:
    def __init__(self):
        self.debug_steps = []
        self.add_face_rectangles_mutation()

    @staticmethod
    def add_face_rectangles(frame):
        face_classifier = FaceClassifier()
        faces = face_classifier.detect_faces(frame)
        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    def add_face_rectangles_mutation(self):
        self.debug_steps.append(FrameDebugger.add_face_rectangles)

    def debug(self, frame):
        for step in self.debug_steps:
            step(frame)