'''
Module providing functionality for initializing and manipulating
a servo motor.

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

_g_PWM_FREQ = 50    # PWM frequency in HZ
_g_MIN_ANGLE = 0    # Minimum servo rotation in degrees
_g_MAX_ANGLE = 180  # Maximum servo rotation in degrees

# TODO Tune these parameters
_g_FULL_LEFT_DC = 2     # Duty cycle for minimum angle
_g_FULL_RIGHT_DC = 10   # Duty cycle for maximum angle


def init(ctrl_pin):
    '''
    Initializes specified pin for PWM control with servo

    :param ctrl_pin: PWM pin to use for servo control
    '''
    assert (ctrl_pin in pins.PWM_PINS), 'Given pin must be a PWM capable pin'

    global _g_initialized
    global _g_pwm_channel
    global _g_conversion_factor

    _g_initialized = False

    # Configure pin for PWM
    _g_pwm_channel = ctrl_pin

    PWM.start(channel=ctrl_pin,
              duty_cycle=_g_FULL_LEFT_DC,
              frequency=_g_PWM_FREQ)

    # Determine conversion factor for calculating duty cycle
    # Conversion factor = slope of line -> ((y2 - y1) / (x2 - x1))
    _g_conversion_factor \
        = (_g_FULL_RIGHT_DC - _g_FULL_LEFT_DC) / (_g_MAX_ANGLE - _g_MIN_ANGLE)

    _g_initialized = True


def turn_to_angle(degree):
    '''
    Turns servo to face specified degree relative to LEFT most rotation

    :param degree: Angle for servo to face (MIN <= degree <= MAX)
    '''
    assert (_g_initialized), "Servo was not initialized"

    # Clamp angle between min/max
    if degree < _g_MIN_ANGLE:
        norm_degree = _g_MIN_ANGLE

    elif degree > _g_MAX_ANGLE:
        norm_degree = _g_MAX_ANGLE

    else:
        norm_degree = degree

    # Calculate necessary duty cycle to achieve angle
    duty_cycle = (_g_conversion_factor * norm_degree) + _g_FULL_LEFT_DC

    # Adjust servo angle
    PWM.set_duty_cycle(_g_pwm_channel, duty_cycle)
