from picamera import PiCamera
from time import sleep

cam = PiCamera()
cam.rotation = 90
cam.start_preview()
for i in range(5):
    sleep(5)
    cam.capture('/home/pi/Desktop/image{}.jpg'.format(i))
cam.stop_preview()
exit(0)