import RPi.GPIO as GPIO
from time import sleep as delay
from time import time


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

    # Invert stepper direction by setting a velocity inverse of the current one
    def invert(self):
        self.set_velocity((-1 if self.dir == GPIO.HIGH else 1) * self.vel)

    # TODO: Change step implementation to threaded
    def step_steps(self, steps):
        if steps < 0:
            self.invert()
        to_step = abs(steps)
        for _ in range(to_step):
            GPIO.output(self.stp_pin, GPIO.HIGH)
            delay(self.vel_to_delay(self.vel) / 1000)
            GPIO.output(self.stp_pin, GPIO.LOW)
            delay(self.vel_to_delay(self.vel) / 1000)

    # Move a single step
    def step(self, invert=False):
        self.step_steps(1 if not invert else -1)


class StepperSystem:

    def __init__(self):
        # Init motors and step dict, set motor count to 0 and set running state to False
        self.motors = {}
        self.motor_count = 0
        self.step_count = {}
        self.running = False

    def add_motor(self, stepper_motor):
        # If the argument isn't a stepper, raise error
        if type(stepper_motor) != Stepper:
            raise TypeError("Argument is not of Stepper type")
        # Increment motor count, add motor and init step count to 0
        self.motor_count += 1
        self.motors[self.motor_count] = stepper_motor
        self.step_count[self.motor_count] = 0

    # Assign step components with a list of steps
    def move(self, steps):
        # If the argument isn't a list, raise error
        if type(steps) != list:
            raise TypeError("Argument is not of list type")
        # If the list is not of the same size, raise error
        if len(steps) != self.motor_count:
            raise IndexError("Vector of steps is of incorrect length with a "
                             "delta of {}".format(len(steps) - self.motor_count))
        # Write steps values into internal steps array
        for i, step in enumerate(steps):
            self.step_count[i+1] = step

    # Start movement assigned by the move function
    def start(self):
        # Set state to running and begin timing
        self.running = True
        init_time = time()
        # While there are non zero elements in the steps vector
        while self.steps_left():
            # Iterate throughout motor indices
            for i in range(self.motor_count):
                # If the selected step vector component is non zero
                if self.step_count[i + 1] > 0:
                    # Step the motor and decrement steps count
                    self.motors[i + 1].step()
                    self.step_count[i + 1] -= 1
        # Set state to not running and return run time
        self.running = False
        return time() - init_time

    # Determines if there is a non zero component left in the steps vector
    def steps_left(self):
        for step in self.step_count.items():
            if step: return True
        return False

