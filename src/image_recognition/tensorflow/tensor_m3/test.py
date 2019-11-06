import numpy as np
import tensorflow.compat.v1 as tf
import cv2 as cv
import time
import keyboard
from imutils.video import FPS
from imutils.video import VideoStream

dir='./ssd_mobilenet_v1_coco_2018_01_28/'
capture_id = 0

capture = cv.VideoCapture(capture_id)

print("capture")
print(capture)

if (capture is None):
    print("No video capture found for id="+capture_id)
    quit()


print("Using tensorflow version " + tf.__version__)

# Read the graph.
with tf.io.gfile.GFile(dir+'frozen_inference_graph.pb', 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())

with tf.Session() as sess:
    # Restore session
    sess.graph.as_default()
    tf.import_graph_def(graph_def, name='')

    # Read and preprocess an image.
    keepAlive = True
    while (keepAlive):

        ret, img = capture.read()
        #img = vs.read()
        rows = img.shape[0]
        cols = img.shape[1]
        inp = cv.resize(img, (300, 300))
        inp = inp[:, :, [2, 1, 0]]  # BGR2RGB

        # Run the model
        out = sess.run([sess.graph.get_tensor_by_name('num_detections:0'),
                        sess.graph.get_tensor_by_name('detection_scores:0'),
                        sess.graph.get_tensor_by_name('detection_boxes:0'),
                        sess.graph.get_tensor_by_name('detection_classes:0')],
                    feed_dict={'image_tensor:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})

        # Visualize detected bounding boxes.
        num_detections = int(out[0][0])
        for i in range(num_detections):
            classId = int(out[3][0][i])
            score = float(out[1][0][i])
            bbox = [float(v) for v in out[2][0][i]]
            if score > 0.3:
                x = bbox[1] * cols
                y = bbox[0] * rows
                right = bbox[3] * cols
                bottom = bbox[2] * rows
                cv.rectangle(img, (int(x), int(y)), (int(right), int(bottom)), (125, 255, 51), thickness=2)
        cv.imshow('TensorFlow MobileNet-SSD', img)
        v = cv.waitKey(20)
        if (v == 27):
            keepAlive=False

cv2.destroyAllWindows()

#cv.imshow('TensorFlow MobileNet-SSD', img)
cv.waitKey()