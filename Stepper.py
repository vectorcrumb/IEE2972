import RPi.GPIO as GPIO
from time import sleep as delay


class Stepper:

    def __init__(self, stp_pin, dir_pin, vel=0.5, vel_high=0.3, vel_low=1.4):
        # Store pins, velocity, direction and velocity-delay transforms
        self.stp_pin = stp_pin
        self.dir_pin = dir_pin
        self.vel = vel
        self.dir = GPIO.LOW
        self.vel_to_delay = lambda x: round((vel_high - vel_low) * x + vel_low, 2)
        self.delay_to_vel = lambda y: round((y - vel_low)/(vel_high - vel_low), 2)
        # Configure pin layout to the BCM scheme
        if GPIO.getmode() != GPIO.BCM:
            GPIO.setmode(GPIO.BCM)
        # Setup pins for step and direction on the driver
        GPIO.setup(self.stp_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        # Set pins low
        GPIO.output(self.stp_pin, GPIO.LOW)
        GPIO.output(self.dir_pin, self.dir)

    def set_velocity(self, new_vel):
        # Check bounds
        if abs(new_vel) > 1:
            raise ValueError("Assigned velocity is too high!")
        # Configure direction
        self.dir = GPIO.HIGH if new_vel > 0 else GPIO.LOW
        # Set absolute speed
        self.vel = abs(new_vel)

    def invert(self):
        self.vel = -1 * self.vel

    # TODO: Change step implementation to threaded
    def step(self, steps):
        if steps < 0:
            self.invert()
        to_step = abs(steps)
        for _ in range(to_step):
            GPIO.output(self.stp_pin, GPIO.HIGH)
            delay(self.vel_to_delay(self.vel) / 1000)
            GPIO.output(self.stp_pin, GPIO.LOW)
            delay(self.vel_to_delay(self.vel) / 1000)
