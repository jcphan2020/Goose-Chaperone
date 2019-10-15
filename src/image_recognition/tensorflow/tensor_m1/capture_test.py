# This file is intended to integrate OpenCV and Tensorflow

import numpy as np
import cv2
import tensorflow as tf
import time
import keyboard #have backup for automous mode

capture = cv2.VideoCapture(0)
cv2.namedWindow('display')
default_graph='./tmp/output_graph.pb'
width = 480
height = 270
export_jpg='_info.jpg'

conf_thresh=.3

#take image and return as file
def get_image():
    return cv2.imread(export_jpg)

#take image and return frame data
def take_image():
    print('click')
    ret, frame = capture.read()
    return frame

def display_image(img):
    cv2.imshow('display', img)

with tf.gfile.FastGFile(default_graph, 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())

with tf.Session() as sess:
    sess.graph.as_default()
    tf.import_graph_def(graph_def, name='')
    img = take_image()
    rows = img.shape[0]
    cols = img.shape[1]
    rsz = cv2.resize(img, (width, height))
    rsz = rsz[:,:,[2,1,0]]

    #Execute model (note, may be slow for now)
    out = sess.run([sess.graph.get_tensor_by_name('num_detections:0'),
                    sess.graph.get_tensor_by_name('detection_scores:0'),
                    sess.graph.get_tensor_by_name('detection_boxes:0'),
                    sess.graph.get_tensor_by_name('detection_classes:0')],
                    feed_dict={'image_tensor:0', rsz.reshape(1, rsz.shape[0])})
    #boundry boxes
    num_detections = int(out[0][0])
    for i in range(num_detections):
        classId = int(out[3][0][i])
        score = float(out[1][0][i])
        bbox = [float(v) for v in out[2][0][i]]
        if score > conf_thresh:
            x = bbox[1] * cols
            y = bbox[0] * rows
            right = bbox[3] * cols
            bottom = bbox[2] * rows
            cv.rectangle(img, (int(x), int(y)), (int(right), int(bottom)), (125, 255, 51), thickness=2)

cv.imshow('TensorFlow MobileNet-SSD', img)
cv.waitKey()

"""
keep_alive = True

while keep_alive:
    #img = take_image()
    #display_image(img)
    ret, frame = capture.read()
    cv2.imshow('display', frame)
    k=cv2.waitKey(1)
    #time.sleep(.5)
    if keyboard.is_pressed('x'):
        keep_alive=False

capture.release()
cv2.destroyAllWindows()

"""