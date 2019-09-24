'''
Module providing structure for interacting with stepper motor
via ULN2003 driver board.
'''
import Adafruit_BBIO.GPIO as GPIO
import enum
import math
import time


@enum.unique
class StepCmd(enum.IntEnum):
    '''
    All possible states in step command 'FSM'
    '''
    CMD_01H = 0
    CMD_03H = 1
    CMD_02H = 2
    CMD_06H = 3
    CMD_04H = 4
    CMD_0CH = 5
    CMD_08H = 6
    CMD_09H = 7
    NUM_CMD = 8


class Stepper(object):
    '''
    Structure providing various methods for utilizing stepper via ULN2003
    '''
    STEPS_PER_REV = 4076.0  # Valid value for ULN2003 stepper motor driver
    DEFAULT_RPM = 15  # Valid value for ULN2003 stepper motor driver

    def __init__(self, pinA, pinB, pinC, pinD,
                 steps_per_rev=STEPS_PER_REV, full_step=True):
        '''
        '''
        self.pins = [pinA, pinB, pinC, pinD]

        # Keeps track of stepper's current angle (should start at 0?)
        self.angle = 0

        # Keeps track of next FSM state (i.e. command to call)
        # Initial state of command 'FSM' based on step type
        if full_step:
            self._next_cmd = StepCmd.CMD_03H
        else:
            self._next_cmd = StepCmd.CMD_01H

        # Number of steps in full revolution
        self.steps_per_rev = steps_per_rev

        # Degree change per step
        self._steps_per_deg = self.steps_per_rev / 360.0

        # Flag indicating whether half or full step should be utilized
        self.full_step = full_step

        # Initialize pins for GPIO output
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)

        # Using tuples as these pin mappings should not be mutable
        # Map commands to high pins -> {Cmd: (pins, set, high)}
        self._cmd_mapping_high = {
            StepCmd.CMD_01H: (pinA,),
            StepCmd.CMD_03H: (pinA, pinB),
            StepCmd.CMD_02H: (pinB,),
            StepCmd.CMD_06H: (pinB, pinC),
            StepCmd.CMD_04H: (pinC,),
            StepCmd.CMD_0CH: (pinC, pinD),
            StepCmd.CMD_08H: (pinD,),
            StepCmd.CMD_09H: (pinD, pinA)
        }

        # Map commands to low pins -> {Cmd: (pins, set, low)}
        self._cmd_mapping_low = {
            StepCmd.CMD_01H: (pinB, pinC, pinD),
            StepCmd.CMD_03H: (pinC, pinD),
            StepCmd.CMD_02H: (pinA, pinC, pinD),
            StepCmd.CMD_06H: (pinA, pinD),
            StepCmd.CMD_04H: (pinA, pinB, pinD),
            StepCmd.CMD_0CH: (pinA, pinB),
            StepCmd.CMD_08H: (pinA, pinB, pinC),
            StepCmd.CMD_09H: (pinB, pinC)
        }

    def __reset_pins(self):
        '''
        '''
        for pin in self.pins:
            GPIO.output(pin, GPIO.LOW)

    def __send_cmd(self, cmd):
        '''
        '''
        try:
            high_pins = self._cmd_mapping_high[cmd]
            low_pins = self._cmd_mapping_low[cmd]
        except KeyError:
            raise ValueError('%s is not a supported step command' % cmd.name)

        # Set pins appropriately
        for pin in high_pins:
            GPIO.output(pin, GPIO.HIGH)

        for pin in low_pins:
            GPIO.output(pin, GPIO.LOW)

    def rotate(self, degrees, rpm=DEFAULT_RPM):
        '''
        '''
        # Time between steps in seconds
        step_delay = 60.0 / (self.steps_per_rev * rpm)

        # Number of steps to rotate (floor and convert to int)
        steps = int(math.fabs(degrees * self._steps_per_deg))

        # Full step and direction calculations
        # TODO Clean this section up and keep track of stepper's angle
        if self.full_step:
            direction = 2
        else:
            direction = 1
            step_delay /= 2  # Twice the steps means half the delay

        if degrees < 0:
            direction *= -1

        # Begin rotation
        for step in range(steps):
            # Send and wait
            self.__send_cmd(self._next_cmd)
            time.sleep(step_delay)

            # Determine next command to send
            self._next_cmd = (self._next_cmd + direction) % StepCmd.NUM_CMD

        # Set pins to low to hold the stepper's angle
        self.__reset_pins()


if __name__ == "__main__":
    stepper = Stepper('a', 'b', 'c', 'd')
    # stepper = Stepper('a', 'b', 'c', 'd', full_step=False)
    stepper.rotate(1)