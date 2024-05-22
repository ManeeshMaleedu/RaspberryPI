from picamera import PiCamera
from time import sleep

class CameraModule:
       def __init__(self):
          self.camera = PiCamera()

       def capture_photo(self, filename):
           self.camera.start_preview()
           sleep(2)
           self.camera.capture(filename)
           self.camera.stop_preview()
