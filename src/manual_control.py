'''"Client" for the manual control logic'''
import msvcrt
from shared import command
import socket

_g_BOT_ADDR = '192.168.7.2'
_g_BOT_PORT = 13131


def run():
    running = True
    movement_speed = 1  # MotorSpeedEnum.SLOW

    bot_addr = (_g_BOT_ADDR, _g_BOT_PORT)
    opt_value = 1  # Set the socket options

    # Initialize client socket with appropriate options
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, opt_value)

    while running:
        key = msvcrt.getch().decode()

        if key == 'q':
            # Exit
            cmd = command.Exit.pack()
            sock.sendto(cmd, bot_addr)
            running = False

        elif key == 'w':
            # Forward
            cmd = command.Move.pack(0, movement_speed)
            sock.sendto(cmd, bot_addr)

        elif key == 's':
            # Reverse
            cmd = command.Move.pack(1, movement_speed)
            sock.sendto(cmd, bot_addr)

        elif key == 'a':
            # Turn left
            cmd = command.Turn.pack(0, 15)  # 0 == TurnDirectionEnum.LEFT
            sock.sendto(cmd, bot_addr)

        elif key == 'd':
            # Turn right
            cmd = command.Turn.pack(1, 15)  # 1 == TurnDirectionEnum.RIGHT
            sock.sendto(cmd, bot_addr)

        else:
            pass


if __name__ == '__main__':
    run()
