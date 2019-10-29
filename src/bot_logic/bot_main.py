import argparse as ap
import Adafruit_BBIO.GPIO as GPIO
import cmd_listener
import constant
# from peripherals import camera
from peripherals import dc_motor_controller as dcmc
from peripherals import stepper
from position import Location
from shared import pins

# Config variables
DevMode = False
ForceRealtimeCamera = False
IdleCaptureRate = 2
EnableLogging = False
LocBuffer = 30

loc = None


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


def init_system():
    global g_panning_stepper

    # Turn on LED indicating that the system is running
    GPIO.setup(constant.RUNNING_LED_PIN, GPIO.OUT)
    GPIO.output(constant.RUNNING_LED_PIN, GPIO.HIGH)

    try:
        # Retrieve command line arguments
        init_cli_options()

        # Initialize peripherals
        # loc.start()

        dcmc.init(constant.L_MOTOR_PWM_PIN, constant.L_MOTOR_SEL_PIN,
                  constant.R_MOTOR_PWM_PIN, constant.R_MOTOR_SEL_PIN,
                  constant.MOTOR_DRIVER_MODE_PIN)

        # camera.init(constant.CAM_CAP_DELAY_MS)

        # g_panning_stepper = stepper.Stepper(constant.PAN_STEPPER_AIN_PIN,
        #                                      constant.PAN_STEPPER_BIN_PIN,
        #                                      constant.PAN_STEPPER_CIN_PIN,
        #                                      constant.PAN_STEPPER_DIN_PIN)

        cmd_listener.start()
    except Exception:
        raise
    finally:
        # Cleanup
        GPIO.output(constant.RUNNING_LED_PIN, GPIO.LOW)
        GPIO.cleanup()

    print("Bot Init")


if __name__ == "__main__":
    print("Starting Bot")
    init_system()
