'''
Module providing GPIO pin constants for working with pin names
on both of the Beaglebone Black's expansion headers.
'''
# **NOTE**  Use the lists to ensure pins are not being misused.
#           Ex: assert (pin in AIN_PINS), 'Pin must be analog input pin'

# PWM
# **NOTE**  EHRPWM chips have 2 output channels hence notations 'A' and 'B'
#           Each channel must have same frequency but can have different
#           duty cycle
PWM0A = 'P9_22'
PWM0B = 'P9_21'
PWM1A = 'P9_14'
PWM1B = 'P9_16'
PWM2A = 'P8_19'
PWM2B = 'P8_13'

PWM_PINS = [PWM0A, PWM0B, PWM1A, PWM1B, PWM2A, PWM2B]


# Single Mode Pins
# **NOTE**  The following are single mode pins (non-configurable).

# Reference voltage pins (3.3V)
# Max Current: 250 mA
REFV_33_PINS = ['P9_3', 'P9_4']

# Reference voltage pins (5V)
# Max Current: 1000 mA
# **NOTE**  Only work when DC power jack connected
REFV_5_PINS = ['P9_5', 'P9_6']

# System voltage pins (5V)
# Max Current: 250 mA
SYSV_PINS = ['P9_7', 'P9_8']

# System reset pin
# **NOTE**  During software startup, initially wait for this pin to be driven
#           HIGH before continuing (System Reference Guide Pg. 82)
SYSR_PIN = 'P9_10'

# Digital grounding pins
DGND_PINS = ['P8_1', 'P8_2', 'P9_1', 'P9_2',
             'P9_43', 'P9_44', 'P9_45', 'P9_46']

# Analog reference voltage pin
REFAV_18_PINS = 'P9_32'

# Analog grounding pin
AGND_PINS = 'P9_34'

# Analog input pins
AIN0 = 'P9_39'
AIN1 = 'P9_40'
AIN2 = 'P9_37'
AIN3 = 'P9_38'
AIN4 = 'P9_33'
AIN5 = 'P9_36'
AIN6 = 'P9_35'

AIN_PINS = [AIN0, AIN1, AIN2, AIN3, AIN4, AIN5, AIN6]
