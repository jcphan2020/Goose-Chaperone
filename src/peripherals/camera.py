'''Module for controlling the capture device on the system'''
# NOTE  'Frame' objects returned from VideoCapture.read() consist of
#       a matrix of data representing the image. This matrix can be
#       maniputlated/analyzed with various OpenCV functions.
import cv2

_g_CAPTURE_DEVICE_INDEX = 0  # Only one camera on system so '0' index
_g_INIT_FRAMES = 5  # Number of throwaway frames to initialize camera


def init(cap_delay):
    '''Creates handle and initializes capture capture device'''
    global _g_vcap  # Handle for capture device
    global _g_cap_delay_ms  # Delay between batch captures in ms

    # Create the object for capturing frames
    _g_vcap = cv2.VideoCapture(_g_CAPTURE_DEVICE_INDEX)
    if not _g_vcap.isOpened():
        raise RuntimeError('Unable to connect to camera.')

    _g_cap_delay_ms = cap_delay

    # Set device properties here if necessary (i.e. frame width/height)
    # Initialize device by capturing dummy frames
    for i in range(_g_INIT_FRAMES):
        _g_vcap.read()
        cv2.waitKey(_g_cap_delay_ms)  # Delay


def release():
    '''Releases the handle on the capture device'''
    _g_vcap.release()


def single_capture():
    '''
    Captures a single frame from the capture device

    :returns: True if frame read correctly along with corresponding frame
    '''
    return _g_vcap.read()


def batch_capture(num):
    '''
    Captures a series of frames with fixed delay between each frame. If an
    invalid frame is encountered in will be thrown away with no retry.

    :param num: Maximum number of frames to capture
    :returns: List of valid frames captured
    '''
    frame_list = []

    if num:
        for i in range(num):
            success, frame = single_capture()

            if success:
                frame_list.append(frame)

            cv2.waitKey(_g_cap_delay_ms)  # Delay

    return frame_list
