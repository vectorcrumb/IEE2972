from picamera.array import PiRGBArray
from picamera import PiCamera
import subprocess as sp
import time
from StepperControls import Stepper, StepperSystem
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


# Pin connections from RasPi to Pololu drivers
DIR_1 = 21
STP_1 = 20
DIR_2 = 26
STP_2 = 19
DIR_3 = 13
STP_3 = 6

# Setup output pins
motor1 = Stepper(STP_1, DIR_1)
motor2 = Stepper(STP_2, DIR_2)
motor3 = Stepper(STP_3, DIR_3)

# Init camera
cam = PiCamera()
# Grab ref to raw cam capture
raw_cap = PiRGBArray(cam)
# Wait on camera init
time.sleep(0.1)
# Grab an image
cam.capture(raw_cap, format="bgr")
img = raw_cap.array
# Display image
print("Still image:", img.shape)

# To obtain video, we'll use the raw_cap
cam.resolution = (640, 480)
cam.framerate = 32
raw_cap = PiRGBArray(cam, size=(640, 480))
# Wait on camera sensor
time.sleep(0.1)
# Capture frames on loop from camera
for frame in cam.capture_continuous(raw_cap, format="bgr", use_video_port=True):
    # Fetch frame
    img = frame.array
    # Display image
    print("Video frame:", img.shape)
    # IMPORTANT: Clear the stream for next frame
    raw_cap.truncate(0)
    break

try:
    # Obtain IK coords
    ann_output = sp.check_output(['./ann', '0.1186', '-0.0464', '59.9701'], cwd='/home/pi')
    ik_coords = list(map(float, ann_output.decode().strip().split('\n')))[3:]
    print("IK Coordinates:", ik_coords)
    # Run code in loop
    while True:
        motor1.step_steps(100)
        motor2.step_steps(100)
        motor3.step_steps(100)
        time.sleep(0.5)
        print("Running stepper control!")
        break
except KeyboardInterrupt:
    # Run a cleanup in case of a keyboard exception
    GPIO.cleanup()
# Cleanup and exit
print("Finished. Ran {} steps per motor!".format(100))
GPIO.cleanup()
exit()
