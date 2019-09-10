'''
Module providing functionality for manipulating system's DC motors
'''
import dc_motor as dcm
import enum
from shared import pins
import time

_g_L_MOTOR_INDEX = 0        # Index of left motor in motor list
_g_R_MOTOR_INDEX = 1        # Index of right motor in motor list
_g_PWM_FREQ = 2000          # PWM frequency in HZ

# TODO Fine tune duty cycles for motors
_g_L_DCYCLES = {dcm.MotorSpeedEnum.STOP: 0, dcm.MotorSpeedEnum.SLOW: 10,
                dcm.MotorSpeedEnum.PATROL: 30, dcm.MotorSpeedEnum.FAST: 75,
                dcm.MotorSpeedEnum.TURN: 15}

_g_R_DCYCLES = {dcm.MotorSpeedEnum.STOP: 0, dcm.MotorSpeedEnum.SLOW: 10,
                dcm.MotorSpeedEnum.PATROL: 30, dcm.MotorSpeedEnum.FAST: 75,
                dcm.MotorSpeedEnum.TURN: 15}


@enum.unique
class TurnDirectionEnum(enum.Enum):
    '''
    Enumeration for valid turn directions
    '''
    RIGHT = enum.auto()
    LEFT = enum.auto()


def init(l_channel, l_select, r_channel, r_select):
    '''
    Initializes specified pins for PWM communication with DC motors

    :param l_channel: PWM pin controlling left DC motor's PWM signal
    :param l_select: GPIO pin controlling direction of left DC motor
    :param r_channel: PWM pin controlling right DC motor's PWM signal
    :param r_select: GPIO pin controlling direction of right DC motor
    '''
    # Ensure proper function usage (can be removed/refactored later)
    assert (l_channel in pins.PWM_PINS), 'Given pin must be a PWM capable pin'
    assert (r_channel in pins.PWM_PINS), 'Given pin must be a PWM capable pin'

    global _g_initialized
    global _g_motors

    _g_initialized = False
    _g_motors = [None, None]

    # Initialize both of system's DC motors
    _g_motors[_g_L_MOTOR_INDEX] = dcm.DCMotor(l_channel,
                                              l_select,
                                              _g_PWM_FREQ,
                                              _g_L_DCYCLES)

    _g_motors[_g_R_MOTOR_INDEX] = dcm.DCMotor(r_channel,
                                              r_select,
                                              _g_PWM_FREQ,
                                              _g_R_DCYCLES)

    _g_initialized = True


def set_speed(setpoint, direction):
    '''
    Sets the base speed for DC motors

    :param setpoint: Speed to set motors
    :param direction: Motor direction
                      0 for forward, 1 for reverse, don't care for braking
    '''
    # Ensure proper function usage (can be removed/refactored later)
    assert (_g_initialized), "DC Motors were not initialized"

    try:
        dcm.MotorSpeedEnum(setpoint)
    except ValueError:
        raise AssertionError('Invalid motor speed setting')

    # Set both motors to the same speed and direction
    for motor in _g_motors:
        motor.set_speed(setpoint, direction)


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
    orig_setpoint = _g_motors[_g_L_MOTOR_INDEX].setpoint

    # Stop the robot
    stop_time = 0.5
    set_speed(dcm.MotorSpeedEnum.STOP)

    time.sleep(stop_time)

    # TODO Calculate time to turn based on how far turn is
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
    set_speed(orig_setpoint)
