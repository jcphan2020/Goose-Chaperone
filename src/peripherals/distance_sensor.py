'''Driver for intializing/utilizing HC-SR04 ultrasonic sensor'''
import Adafruit_BBIO.GPIO as GPIO
import time

_g_TRIGGER_PULSE_S = 0.00001  # Trigger pulse length (in seconds) = 10us
_g_ECHO_START_TIMEOUT_MS = 25  # Wait time for echo return (approx. dist 425cm)
_g_ECHO_END_TIMEOUT_MS = 12.5  # Time to wait for echo to end
_g_SOUND_SPEED = 34300  # Speed of sound (cm/s) in air
_g_initialized = False


class UltrasonicSensor(object):
    '''Structure for HC-SR04 ultrasonic sensor pins'''
    def __init__(self, trigger, echo):
        self.trigger_pin = trigger
        self.echo_pin = echo


def init(trigger, echo):
    '''
    Initializes specified pins to work with distance sensor

    :param trigger: Pin to trigger ultrasonic burst
    :param echo: Pin for detecting the echo pulse
    '''
    global _g_initialized
    global g_sensor

    # Ensure proper function usage (can be removed/refactored later)
    assert (not _g_initialized), 'Distance sensor already initialized'

    # Initialize distance sensor structure and pins
    g_sensor = UltrasonicSensor(trigger, echo)
    GPIO.setup(g_sensor.trigger_pin, GPIO.OUT)
    GPIO.setup(g_sensor.echo_pin, GPIO.IN)

    _g_initialized = True
    print('Distance Sensor Initialized')


def detect_distance():
    '''
    Take a distance reading from the ultrasonic sensor

    :returns: Distance if object detected, -1 otherwise
    '''
    # Ensure proper function usage (can be removed/refactored later)
    assert (_g_initialized), 'Distance sensor was not initialized'

    distance = -1
    end_edge_detect = None

    # Execute sensor trigger (10us pulse)
    GPIO.output(g_sensor.trigger_pin, GPIO.HIGH)
    time.sleep(_g_TRIGGER_PULSE_S)
    GPIO.output(g_sensor.trigger_pin, GPIO.LOW)

    # Listen for echo
    # TODO wait_for_edge function needs testing
    start_edge_detect = GPIO.wait_for_edge(g_sensor.echo_pin,
                                           GPIO.RISING,
                                           _g_ECHO_START_TIMEOUT_MS)

    if start_edge_detect:
        # Record start time of echo (in seconds)
        echo_pulse_start = time.time()

        # Wait for end of echo pulse
        end_edge_detect = GPIO.wait_for_edge(g_sensor.echo_pin,
                                             GPIO.FALLING,
                                             _g_ECHO_END_TIMEOUT_MS)

    if end_edge_detect:
        # Calculate the time echo pulse spent high
        echo_pulse_end = time.time()
        pulse_width = echo_pulse_end - echo_pulse_start  # Echo pulse duration

        # Calculate the distance in centimeters (divide by 2 due to round trip)
        distance = (pulse_width * _g_SOUND_SPEED) / 2

    return distance


def cleanup():
    '''Sets all GPIO signals low'''
    # Ensure proper function usage (can be removed/refactored later)
    assert (_g_initialized), 'Distance sensor was not initialized'

    GPIO.output(g_sensor.trigger_pin, GPIO.LOW)
    GPIO.output(g_sensor.echo_pin, GPIO.LOW)


# Original Code
# # HC-SR04 connection
# vcc = "5V"
# trigger = "GPIO_66"
# echo = "P8_8"
# gnd = "GND"

# GPIO.cleanup()
# time.sleep(2)


# def distance_measurement(TRIG, ECHO):
#     GPIO.output(TRIG, True)
#     time.sleep(0.00001)
#     GPIO.output(TRIG, False)
#     pulseStart = time.time()
#     pulseEnd = time.time()
#     counter = 0
#     while GPIO.input(ECHO) == 0:
#         pulseStart = time.time()
#         counter += 1
#     while GPIO.input(ECHO) == 1:
#         pulseEnd = time.time()

#     pulseDuration = pulseEnd - pulseStart
#     distance = pulseDuration * 17150
#     distance = round(distance, 2)
#     return distance


# # Configuration
# print("trigger: [{}]".format(trigger))
# GPIO.setup(trigger, GPIO.OUT)  # Trigger
# print("echo: [{}]".format(echo))
# GPIO.setup(echo, GPIO.IN)  # Echo
# GPIO.output(trigger, False)
# print("Setup completed!")

# # Security
# GPIO.output(trigger, False)
# time.sleep(0.5)

# distance = distance_measurement(trigger, echo)
# while True:
#     print("Distance: [{}] cm.".format(distance))
#     time.sleep(2)
#     if distance <= 5:
#         print("Too close! Exiting...")
#         break
#     else:
#         distance = distance_measurement(trigger, echo)

# GPIO.cleanup()
# print("Done")
