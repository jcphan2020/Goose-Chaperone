'''Controller for manipulating system's two DC motors via DRV8835 driver'''
import Adafruit_BBIO.GPIO as GPIO
from . import drv8835_dc_motor as dcm
import enum
from shared import pins
import time

_g_L_MOTOR_INDEX = 0        # Index of left motor in motor list
_g_R_MOTOR_INDEX = 1        # Index of right motor in motor list
_g_DRIVER_MODE_PHASE_ENABLE = GPIO.HIGH     # DRV8835 PHASE/ENABLE mode
_g_DRIVER_MODE_IN_IN = GPIO.LOW             # DRV8835 IN/IN mode

# TODO Fine tune duty cycles for motors
# Motor Speed Setting: Duty Cycle
_g_L_DCYCLES = {dcm.MotorSpeedEnum.STOP: 0, dcm.MotorSpeedEnum.SLOW: 15,
                dcm.MotorSpeedEnum.PATROL: 25, dcm.MotorSpeedEnum.FAST: 40,
                dcm.MotorSpeedEnum.TURN: 15}

_g_R_DCYCLES = {dcm.MotorSpeedEnum.STOP: 0, dcm.MotorSpeedEnum.SLOW: 15,
                dcm.MotorSpeedEnum.PATROL: 25, dcm.MotorSpeedEnum.FAST: 40,
                dcm.MotorSpeedEnum.TURN: 15}


@enum.unique
class TurnDirectionEnum(enum.Enum):
    '''Enumeration for valid turn directions'''
    LEFT = 0
    RIGHT = 1


def init(l_channel, l_select, r_channel, r_select, mode_sel):
    '''
    Initializes specified pins for PWM communication with DC motors

    :param l_channel: PWM pin controlling left DC motor's PWM signal
    :param l_select: GPIO pin controlling direction of left DC motor
    :param r_channel: PWM pin controlling right DC motor's PWM signal
    :param r_select: GPIO pin controlling direction of right DC motor
    :param mode_sel: GPIO pin controlling mode of DRV8835 motor driver
    '''
    # Ensure proper function usage (can be removed/refactored later)
    assert (l_channel in pins.PWM_PINS), 'Given pin must be a PWM capable pin'
    assert (r_channel in pins.PWM_PINS), 'Given pin must be a PWM capable pin'

    global _g_initialized
    global _g_motors
    global _g_mode_sel

    _g_initialized = False
    _g_motors = [None, None]

    # Initialize both of system's DC motors
    _g_motors[_g_L_MOTOR_INDEX] = dcm.DCMotor(l_channel,
                                              l_select,
                                              _g_L_DCYCLES)

    _g_motors[_g_R_MOTOR_INDEX] = dcm.DCMotor(r_channel,
                                              r_select,
                                              _g_R_DCYCLES)

    # Set the DRV8835 mode to PHASE/ENABLE for simplest usage
    _g_mode_sel = mode_sel
    GPIO.setup(_g_mode_sel, GPIO.OUT)
    GPIO.output(_g_mode_sel, _g_DRIVER_MODE_PHASE_ENABLE)

    _g_initialized = True
    print('DC Motor Controller Initialized')


def cleanup():
    '''
    Shutsdown the DC motor contol
    '''
    for motor in _g_motors:
        motor.cleanup()

    GPIO.output(_g_mode_sel, GPIO.LOW)
    print('DC Motor Controller shutdown')


def set_speed(speed_setting, direction=None):
    '''
    Sets the base speed for DC motors

    :param speed_setting: Speed to set motors
    :param direction: Motor direction
                      0 for forward, 1 for reverse, don't care for braking
    '''
    # Ensure proper function usage (can be removed/refactored later)
    assert (_g_initialized), "DC Motors were not initialized"

    try:
        speed = dcm.MotorSpeedEnum(speed_setting)
    except ValueError:
        raise AssertionError('Invalid motor speed setting')

    # Set both motors to the same speed and direction
    for motor in _g_motors:
        motor.set_speed(speed, direction)


def stop():
    '''Method for bringing DC motors to a stop'''
    set_speed(dcm.MotorSpeedEnum.STOP)


def __normalize_turn(degree, direction):
    '''
    Normalizes turn instructions (i.e. 271 LEFT -> 89 RIGHT)

    :param degree: How many degrees to turn
    :param direction: Direction to turn
    '''
    # No purpose in making full rotation
    norm_degr = degree % 360
    norm_dir = direction

    # Max turn should be 180 degrees
    if norm_degr > 180:
        # Switch turn direction
        norm_degr = 360 - norm_degr

        if direction == TurnDirectionEnum.LEFT:
            norm_dir = TurnDirectionEnum.RIGHT
        else:
            norm_dir = TurnDirectionEnum.LEFT

    return norm_degr, norm_dir


def turn(degree, direction):
    '''
    Performs sequence of events to turn

    :param degree: How many degrees to turn (degree fractions get truncated)
    :param direction: Direction to turn
    '''
    # Ensure proper function usage (can be removed/refactored later)
    assert (_g_initialized), 'DC Motors were not initialize'
    assert (degree >= 0), 'Must pass positive degree to \'turn\' function'
    assert (type(degree) is not float), 'Degree fractions not allowed'

    try:
        TurnDirectionEnum(direction)
    except ValueError:
        raise AssertionError('Invalid turn direction')

    # Normalize degree and direction
    # Convert to integer if necessary (will truncate fractions of degree)
    norm_degr, norm_dir = __normalize_turn(int(degree), direction)

    # Record current speed
    orig_speed_setting = _g_motors[_g_L_MOTOR_INDEX].speed_setting

    # Stop the robot
    stop_time = 0.5
    stop()

    time.sleep(stop_time)

    # TODO Calculate time to turn based on degrees
    turn_time = 1.0

    # Turn robot
    if norm_dir == TurnDirectionEnum.LEFT:
        _g_motors[_g_L_MOTOR_INDEX].set_speed(dcm.MotorSpeedEnum.TURN, 1)
        _g_motors[_g_R_MOTOR_INDEX].set_speed(dcm.MotorSpeedEnum.TURN, 0)
    else:
        _g_motors[_g_R_MOTOR_INDEX].set_speed(dcm.MotorSpeedEnum.TURN, 1)
        _g_motors[_g_L_MOTOR_INDEX].set_speed(dcm.MotorSpeedEnum.TURN, 0)

    time.sleep(turn_time)

    # Restore original speed
    set_speed(orig_speed_setting)
