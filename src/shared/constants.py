'''
Defines constants for pinouts, channels, general configurations,
and system messages
'''
from shared import pins

# Configurations for pinouts
ALERT_LED_PIN = 1  # Example, if we want to have an LED status light
RUNNING_LED_PIN = 'USR1'  # LED indicating the system is up and running

L_MOTOR_PWM_PIN = pins.PWM2B  # DC Motor pinout
L_MOTOR_SEL_PIN = 'P8_14'
R_MOTOR_PWM_PIN = pins.PWM2A
R_MOTOR_SEL_PIN = 'P8_16'
MOTOR_DRIVER_MODE_PIN = 'P8_18'

PAN_STEPPER_AIN_PIN = 'P9_15'  # Stepper for panning camera/sensor pinout
PAN_STEPPER_BIN_PIN = 'P9_23'
PAN_STEPPER_CIN_PIN = 'P9_25'
PAN_STEPPER_DIN_PIN = 'P9_27'

# Alert Messages

# Other configs
SYSTEM_RESET_TIMEOUT_MS = 2000  # Time to wait for system to initialize
UART_BAUD = 9600
CAM_CAP_DELAY_MS = 20  # Delay between camera batch captures in ms