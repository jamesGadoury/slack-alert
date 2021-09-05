import cv2

class VideoCaptureWindow:
    def __init__(self, name='VideoCapture', width=1280, height=720):
        self.name = name
        self.width = width
        self.height = height

    def generate(self):
        cv2.namedWindow(self.name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.name, self.width, self.height)

    def updateFrame(self, frame):
        cv2.imshow(self.name, frame)

    def destroy(self):
        cv2.destroyWindow(self.name)