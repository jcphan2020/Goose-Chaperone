import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import argparse as ap
import cmd_listener
import comvis as cs
# from peripherals import camera
from peripherals import distance_sensor as dsense
from peripherals import TB67H420FTG_motor_driver as dcmc
from peripherals import uln2003_stepper as smotor
from position import Location
from shared import constants
from time import sleep

# Config variables
DevMode = False
ForceRealtimeCamera = False
IdleCaptureRate = 2
EnableLogging = False
LocBuffer = 30

loc = None

BOOT_ALERT = 0          #Has started boot
START_ALERT = 1         #Begining operation
FAIL_START_ALERT = 2    #Failed to start
SHUTDOWN_ALERT = 3      #Shutting down

def init_cli_options():
    # Define Command Line Arguments
    arg_parse = ap.ArgumentParser(description='Modify starting parameters')
    arg_parse.add_argument(
        '--dev_mode',
        type=bool,
        default=False,
        help='Enable development mode')

    arg_parse.add_argument(
        '--force_realtime_camera',
        type=bool,
        default=False,
        help='If set to true, power saving burst recognition mode is disabled')

    arg_parse.add_argument(
        '--capture_rate',
        type=int,
        default=2,
        help='Maximum number of photos taken and analyzed per second')

    arg_parse.add_argument(
        '--logging',
        type=bool,
        default=False,
        help='Create and append log files')

    arg_parse.add_argument(
        '--pos_buffer',
        type=int,
        default=30,
        help='GPS coordinate buffer capacity')

    args = arg_parse.parse_args()
    DevMode = args.dev_mode
    ForceRealtimeCamera = args.force_realtime_camera
    IdleCaptureRate = args.capture_rate
    EnableLogging = args.logging
    LocBuffer = args.pos_buffer

    global loc
    loc = Location(LocBuffer, test)
    print(loc)
    print(args)
    print("CLI")


def test():  # Placeholder for GPS data gathering function, replace.
    print("Weeee")

def flashLED(time, occurences, end_mode):
    for i in range(0, occurences):
        if (i%2==0):
            GPIO.output(constants.RUNNING_LED_PIN, GPIO.HIGH)
        else:
            GPIO.output(constants.RUNNING_LED_PIN, GPIO.LOW)
        i+=1
        sleep(time)
    if (end_mode==0):
        GPIO.output(constants.RUNNING_LED_PIN, GPIO.LOW)
    else:
        GPIO.output(constants.RUNNING_LED_PIN, GPIO.HIGH)


def alertLED(mode):
    if (mode == BOOT_ALERT):
        flashLED(0.2, 6, 1)
    elif (mode == START_ALERT):
        flashLED(0.1, 10, 1)
    elif (mode == FAIL_START_ALERT):
        flashLED(1,5,0)
    else:
        flashLED(.1,10,0)


def init_system():
    # Turn on LED indicating that the system is running
    GPIO.setup(constants.RUNNING_LED_PIN, GPIO.OUT)
    GPIO.output(constants.RUNNING_LED_PIN, GPIO.HIGH)

    alertLED(START_ALERT)

    try:

        # Retrieve command line arguments
        init_cli_options()

        # Initialize peripherals
        # loc.start()

        # dcmc.init(constants.L_MOTOR_PWM_PIN,
        #           constants.L_MOTOR_SEL1_PIN, constants.L_MOTOR_SEL2_PIN,
        #           constants.R_MOTOR_PWM_PIN,
        #           constants.R_MOTOR_SEL1_PIN, constants.R_MOTOR_SEL2_PIN)

        # camera.init(constants.CAM_CAP_DELAY_MS)

        # smotor.init(constants.PAN_STEPPER_AIN_PIN,
        #             constants.PAN_STEPPER_BIN_PIN,
        #             constants.PAN_STEPPER_CIN_PIN,
        #             constants.PAN_STEPPER_DIN_PIN)

        # dsense.init(constants.DIST_SENSOR_TRIGGER_PIN,
        #             constants.DIST_SENSOR_ECHO_PIN)

        # Startup bot's mainloop or manual control
        cmd_listener.start()

        loop()
    except Exception:
        alertLED(FAIL_START_ALERT)
        raise
    finally:
        # Cleanup
        GPIO.output(constants.RUNNING_LED_PIN, GPIO.LOW)
        dcmc.cleanup()
        GPIO.cleanup()
        PWM.cleanup()
        alertLED(SHUTDOWN_ALERT)

def loop():
    #Scan for targets
    keepAlive = True
    bird_count = 0
    human_count = 0
    while(keepAlive):
        r = cs.get_detections()
        i=0
        while i<len(r):
            if (r[i][cs.CLASSES_IDX] == cs.HUMAN):
                print("Do Human Action")
                human_count += 1
            if (r[i][cs.CLASSES_IDX] == cs.BIRD):
                print("Do Bird Action")
                bird_count += 1
            i+=1

    #Scan for obstacles

    #Control movement based on bird, human count


if __name__ == "__main__":
    print("Starting Bot...")
    init_system()
