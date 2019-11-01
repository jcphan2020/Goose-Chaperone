'''Driver for initializing and utilizing a DC motor.'''
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import enum

_g_SPD_DIR_VALUES = [0, 1, None]    # Valid values for speed direction


@enum.unique
class MotorSpeedEnum(enum.Enum):
    '''Enumeration for all valid speed settings'''
    STOP = 0
    SLOW = 1
    PATROL = 2
    FAST = 3
    TURN = 4


class DCMotor(object):
    # PWM frequency in HZ
    # Max PWM freq for DRV8835 Motor Driver = 250 kHz
    _PWM_FREQ_HZ = 20000

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
                  frequency=DCMotor._PWM_FREQ_HZ)

        # Configure GPIO pin controlling motor direction
        GPIO.setup(self.select, GPIO.OUT)

        print('DC Motor Initialized - PWM: %s  SEL: %s' % (self.channel,
                                                           self.select))

    def set_speed(self, speed_setting, direction=None):
        '''
        Sets the motor speed for the motor

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
        print('Set PWM \'%s\' duty cycle: %d%%' % (self.channel, dcycle))

    def cleanup(self):
        '''
        Stops PWM channel
        '''
        PWM.stop(self.channel)
        GPIO.output(self.select, GPIO.LOW)
        print('DC Motor shutdown')
