import cv2

class VideoCaptureWindow:
    QUIT_BUTTON = 'quit'
    PAUSE_BUTTON = 'pause'
    def __init__(self, name='VideoCapture', width=1280, height=720):
        self.name = name
        self.width = width
        self.height = height

    def generate(self):
        cv2.namedWindow(self.name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.name, self.width, self.height)

    def update_frame(self, frame):
        cv2.imshow(self.name, frame)

    def handle_button_event(self):
        key = cv2.waitKey(1)
        if key == ord('q'):
            return VideoCaptureWindow.QUIT_BUTTON
        if key == ord('p'):
            return VideoCaptureWindow.PAUSE_BUTTON
        return None

    def destroy(self):
        cv2.destroyWindow(self.name)