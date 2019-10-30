'''Allows for manual control of the bot over Ethernet'''
from peripherals import dc_motor_controller as dcmc
from shared import command
import socket

_g_BIND_ADDR = ''
_g_PORT = 13131
_g_RECV_BUF_SIZE = 1024  # Max size of received data in bytes


def start():
    '''Initializes and starts listening for commands'''
    server_addr = (_g_BIND_ADDR, _g_PORT)  # Address to listen at
    opt_value = 1  # Set the socket options

    # Initialize server socket with appropriate options
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, opt_value)

    # Bind to listen to appropriate address
    server.bind(server_addr)

    running = True  # Exit flag

    while running:
        cmd_bytes = server.recv(_g_RECV_BUF_SIZE)  # Block until data

        if cmd_bytes:
            # Parse
            cmd_type = command.parse_cmd_type(cmd_bytes)

            # Act
            if cmd_type == command.MOVE_CMD:
                direction, speed = command.Move.unpack(cmd_bytes)

                if direction == 0:
                    dir_str = 'forward'
                else:
                    dir_str = 'reverse'

                print('--Move Req: \'%s\' at speed setting \'%d\'' % (dir_str,
                                                                      speed))
                dcmc.set_speed(speed, direction)

            elif cmd_type == command.TURN_CMD:
                direction, degrees = command.Turn.unpack(cmd_bytes)

                if direction == 0:
                    dir_str = 'left'
                else:
                    dir_str = 'right'

                print('--Turn Req: %s %d degrees' % (dir_str, degrees))

                dcmc.turn(degrees, dcmc.TurnDirectionEnum(direction))

            elif cmd_type == command.EXIT_CMD:
                running = False
                print('--Exit Req')

            else:
                # Invalid command
                print('Invalid command received')

    # Cleanup
    server.close()
