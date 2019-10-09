'''Module for controlling the capture device on the system'''
# NOTE  'Frame' objects returned from VideoCapture.read() consist of
#       a matrix of data representing the image. This matrix can be
#       maniputlated/analyzed with various OpenCV functions.
import cv2

CAPTURE_DELAY_MS = 10  # How long to delay between batch captures
CAPTURE_DEVICE_INDEX = 0  # Only one camera on system so '0' index
INIT_FRAMES = 5  # Number of throwaway frames to initialize camera


def init():
    '''Creates handle and initializes capture capture device'''
    global vcap

    # Create the object for capturing frames
    vcap = cv2.VideoCapture(CAPTURE_DEVICE_INDEX)
    if not vcap.isOpened():
        raise RuntimeError('Unable to connect to camera.')

    # Set device properties here if necessary (i.e. frame width/height)
    # Initialize device by capturing dummy frames
    for i in range(INIT_FRAMES):
        vcap.read()
        cv2.waitKey(CAPTURE_DELAY_MS)  # Delay


def release():
    '''Releases the handle on the capture device'''
    vcap.release()


def single_capture():
    '''
    Captures a single frame from the capture device

    :returns: True if frame read correctly along with corresponding frame
    '''
    return vcap.read()


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

            cv2.waitKey(CAPTURE_DELAY_MS)  # Delay

    return frame_list
