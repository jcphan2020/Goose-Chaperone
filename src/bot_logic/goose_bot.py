import argparse as ap

import constant

def init_cli_options():
    #Define Command Line Arguments
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

    arg_parse.parse_args()


def init_system():
    init_cli_options()
    print("Bot Init")

if __name__ == "__main__":
    print("Starting Bot")
    init_system()

