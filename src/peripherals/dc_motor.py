'''
Driver for initializing and utilizing a DC motor.
'''
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import enum

_g_SPD_DIR_VALUES = [0, 1, None]    # Valid values for speed direction


class MotorSpeedEnum(enum.Enum):
    '''
    Enumeration for all valid speed settings
    '''
    STOP = enum.auto()
    SLOW = enum.auto()
    PATROL = enum.auto()
    FAST = enum.auto()
    TURN = enum.auto()


class DCMotor(object):
    _PWM_FREQ = 2000  # PWM frequency in HZ

    def __init__(self, channel, select, dcycle_map):
        '''
        Initializes DC motor for PWM communication with specified pin

        :param channel: PWM pin controlling DC motor's PWM signal
        :param select: GPIO pin controlling motor direction
        :param dcycle_map: Mapping between speed setting and duty cycle
        '''
        self.channel = channel
        self.select = select
        self.dcycle_map = dcycle_map
        self.speed_setting = MotorSpeedEnum.STOP

        # Configure PWM channel with initial duty cycle of 0
        PWM.start(channel=self.channel,
                  duty_cycle=0,
                  frequency=DCMotor._PWM_FREQ)

        # Configure GPIO pin controlling motor direction
        GPIO.setup(self.select, GPIO.OUT)

    def set_speed(self, speed_setting, direction=None):
        '''
        Sets the motor speed

        :param speed_setting: Speed setting to set motor to
        :param direction: Motor direction
                          0 for forward, 1 for reverse, None for no change
        '''
        # Ensure proper function usage (can be removed/refactored later)
        assert (direction in _g_SPD_DIR_VALUES), 'Invalid direction' \
                                                 ' for motor speed'

        # Get the appropriate duty cycle
        dcycle = self.dcycle_map[speed_setting]

        # Set direction if necessary
        if direction is not None:
            GPIO.output(self.select, direction)

        # Perform speed change
        PWM.set_duty_cycle(self.channel, dcycle)

        # Track active speed setting
        self.speed_setting = speed_setting
