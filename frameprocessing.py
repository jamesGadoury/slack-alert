import cv2
from faceclassifier import FaceClassifier

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

class MultipleFaceChecker:
    def __init__(self):
        self.face_classifier = FaceClassifier()

    def check(self, frame):
        # Detect faces
        faces = self.face_classifier.detect_faces(frame)
        return len(faces) > 1

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