'''
Driver for initializing and utilizing a servo motor.
NOTE: Relationship between duty cycle and servo angle can be fit on a line

    Duty Cycle (%)
        |
   y2 ? |           o
        |
        |
   y1 ? | o
        |___________________
         min       max      Angle (degrees)
          x1        x2

    Formula to convert angle (x) to duty cycle (y):
        y - y1 = m(x - x1)      where m = (y2 - y1) / (x2 - x1)
'''
import Adafruit_BBIO.PWM as PWM
from shared import pins


class Servo(object):
    '''Structure for interacting with a servo motor over PWM'''
    PWM_FREQ = 50    # PWM frequency in HZ
    MIN_ANGLE = 0    # Minimum servo rotation in degrees
    MAX_ANGLE = 180  # Maximum servo rotation in degrees

    def __init__(self, ctrl_pin, full_left_dc, full_right_dc):
        '''
        Initializes specified pin for PWM control with servo. The full left
        and full right duty cycle should be tuned for each individual servo
        motor.

        :param ctrl_pin: PWM pin to use for servo control
        :param full_left_dc: Duty cycle for servo's minimum angle
        :param full_right_dc: Duty cycle for servo's maximum angle
        '''
        assert (ctrl_pin in pins.PWM_PINS), \
            'Given pin must be a PWM capable pin'
        assert (full_left_dc >= 0 and full_left_dc <= 100), \
            'Duty cycle must be between 0 and 100'
        assert (full_right_dc >= 0 and full_right_dc <= 100), \
            'Duty cycle must be between 0 and 100'

        self.pwm_channel = ctrl_pin
        self.full_left_dc = full_left_dc
        self.full_right_dc = full_right_dc

        # Configure PWM channel
        PWM.start(channel=self.pwm_channel,
                  duty_cycle=self.full_left_dc,
                  frequency=Servo.PWM_FREQ)

        # Determine conversion factor for calculating duty cycle
        # Conversion factor = slope of line -> ((y2 - y1) / (x2 - x1))
        self.conversion_factor                          \
            = (self.full_right_dc - self.full_left_dc)  \
            / (Servo.MAX_ANGLE - Servo.MIN_ANGLE)

    def turn_to_angle(self, degree):
        '''
        Turns servo to face specified degree relative to LEFT most rotation

        :param degree: Angle for servo to face (Clamped: MIN <= degree <= MAX)
        '''
        # Clamp angle between min/max
        if degree < Servo.MIN_ANGLE:
            norm_degree = Servo.MIN_ANGLE

        elif degree > Servo.MAX_ANGLE:
            norm_degree = Servo.MAX_ANGLE

        else:
            norm_degree = degree

        # Calculate necessary duty cycle to achieve angle
        duty_cycle = (self.conversion_factor * norm_degree) \
            + self.full_left_dc

        PWM.set_duty_cycle(self.pwm_channel, duty_cycle)
