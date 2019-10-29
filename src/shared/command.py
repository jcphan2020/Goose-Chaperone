'''Defines different commands for actions that robot can take'''
import struct

EXIT_CMD = 0  # Command types
MOVE_CMD = 1
TURN_CMD = 2

_g_NET_FMT = '!'   # Network(big-endian) byte ordering for packing/unpacking
_g_CMD_TYPE_FMT = 'B'  # 1 byte for command type
_g_CMD_TYPE_LEN = struct.calcsize(_g_CMD_TYPE_FMT)


class Move(object):
    _DIR_FMT = 'B'  # 1 byte for motion direction (0=forward, 1=reverse)
    _SPD_FMT = 'B'  # 1 byte for speed of motion
    _PACK_FMT = _g_NET_FMT + _g_CMD_TYPE_FMT + _DIR_FMT + _SPD_FMT
    _UNPACK_FMT = _g_NET_FMT + _DIR_FMT + _SPD_FMT

    @staticmethod
    def pack(direction, speed):
        return struct.pack(Move._PACK_FMT, MOVE_CMD, direction, speed)

    @staticmethod
    def unpack(byte_data):
        data = byte_data[_g_CMD_TYPE_LEN:]
        return struct.unpack(Move._UNPACK_FMT, data)


class Turn(object):
    _DIR_FMT = 'B'  # 1 byte for motion direction (0=left, 1=right)
    _DEG_FMT = 'H'  # 2 bytes for number of degrees to turn
    _PACK_FMT = _g_NET_FMT + _g_CMD_TYPE_FMT + _DIR_FMT + _DEG_FMT
    _UNPACK_FMT = _g_NET_FMT + _DIR_FMT + _DEG_FMT

    @staticmethod
    def pack(direction, degrees):
        return struct.pack(Turn._PACK_FMT, TURN_CMD, direction, degrees)

    @staticmethod
    def unpack(byte_data):
        data = byte_data[_g_CMD_TYPE_LEN:]
        return struct.unpack(Turn._UNPACK_FMT, data)


class Exit(object):
    _PACK_FMT = _g_NET_FMT + _g_CMD_TYPE_FMT

    @staticmethod
    def pack():
        return struct.pack(Exit._PACK_FMT, EXIT_CMD)


def parse_cmd_type(byte_data):
    cmd_type_bytes = byte_data[:_g_CMD_TYPE_LEN]
    fmt = _g_NET_FMT + _g_CMD_TYPE_FMT

    return struct.unpack(fmt, cmd_type_bytes)
