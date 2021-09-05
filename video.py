import cv2

class VideoCaptureWindow:
    def __init__(self, name='VideoCapture', width=1280, height=720):
        self.name = name
        self.width = width
        self.height = height

    def generate(self):
        cv2.namedWindow(self.name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.name, self.width, self.height)

    def update_frame(self, frame):
        cv2.imshow(self.name, frame)

    def exit_event(self):
      # the 'q' button is set as the quitting button
      return cv2.waitKey(1) & 0xFF == ord('q')

    def destroy(self):
        cv2.destroyWindow(self.name)