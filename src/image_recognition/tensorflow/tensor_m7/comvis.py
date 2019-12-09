import pathlib
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import cv2 as cv
import time
import keyboard
from imutils.video import FPS
from imutils.video import VideoStream

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
from IPython.display import display

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

capture_id = 0
capture = cv.VideoCapture(capture_id)

# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1

# Patch the location of gfile
tf.gfile = tf.io.gfile

def load_model(model_name):
  base_url = 'http://download.tensorflow.org/models/object_detection/'
  model_file = model_name + '.tar.gz'
  model_dir = tf.keras.utils.get_file(
    fname=model_name, 
    origin=base_url + model_file,
    untar=True)

  model_dir = pathlib.Path(model_dir)/"saved_model"

  print(model_dir)

  model_dir='./'

  model = tf.saved_model.load(str(model_dir))
  model = model.signatures['serving_default']

  print(">>>>>>>>>>>>>>")
  print(model_dir)

  return model

  

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = 'models/research/object_detection/data/mscoco_label_map.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

model_name = 'ssd_mobilenet_v1_coco_2017_11_17'
detection_model = load_model(model_name)

PATH_TO_TEST_IMAGES_DIR = pathlib.Path('models/research/object_detection/test_images')
TEST_IMAGE_PATHS = sorted(list(PATH_TO_TEST_IMAGES_DIR.glob("*.jpg")))
TEST_IMAGE_PATHS

#print(category_index)

#TODO adapt to stream
def run_inference(model, image):
  image = np.asarray(image)
  # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
  input_tensor = tf.convert_to_tensor(image)
  # The model expects a batch of images, so add an axis with `tf.newaxis`.
  input_tensor = input_tensor[tf.newaxis,...]

  # Run inference
  output_dict = model(input_tensor)

  # All outputs are batches tensors.
  # Convert to numpy arrays, and take index [0] to remove the batch dimension.
  # We're only interested in the first num_detections.
  num_detections = int(output_dict.pop('num_detections'))
  output_dict = {key:value[0, :num_detections].numpy() 
                 for key,value in output_dict.items()}
  output_dict['num_detections'] = num_detections

  # detection_classes should be ints.
  output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)
   
  # Handle models with masks:
  if 'detection_masks' in output_dict:
    # Reframe the the bbox mask to the image size.
    detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
              output_dict['detection_masks'], output_dict['detection_boxes'],
               image.shape[0], image.shape[1])      
    detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5,
                                       tf.uint8)
    output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()
  #print('----------------')
  #print(detection_classes)
  #print('----------------')

  return output_dict

def show_inference(model, image_path):
  # the array based representation of the image will be used later in order to prepare the
  # result image with boxes and labels on it.
  #image_np = np.array(Image.open(image_path))
  ret,img = capture.read()
  rows = img.shape[0]
  cols = img.shape[1]
  inp = cv.resize(img, (300, 300))
  inp = inp[:, :, [2, 1, 0]]  # BGR2RGB

  image_np = inp
  # Actual detection.
  output_dict = run_inference(model, image_np)
  #print(output_dict)
  '''num_detections = int(output_dict[0][0])
  for i in range(num_detections):
      classId = int(output_dict[3][0][i])
      score = float(output_dict[1][0][i])
      bbox = [float(v) for v in output_dict[2][0][i]]
      if score > 0.3:
          x = bbox[1] * cols
          y = bbox[0] * rows
          right = bbox[3] * cols
          bottom = bbox[2] * rows
          cv.rectangle(img, (int(x), int(y)), (int(right), int(bottom)), (125, 255, 51), thickness=2)
  
  cv.imshow('TensorFlow MobileNet-SSD', img)
  v = cv.waitKey(20)
  if (v == 27):
      keepAlive=False'''
  # Visualization of the results of a detection.
  
  #print(output_dict['detection_boxes'])
  #print(output_dict['detection_classes'])
  #print(output_dict['detection_scores'])
  #print('-------')

  #quit()

  scores = output_dict['detection_scores']

  #print(scores)

  #if (scores[0]>0.5):
   # print("Human detected")
  if (scores[15]>0.5):
    print("Bird detected")

  vis_util.visualize_boxes_and_labels_on_image_array(
      image_np,
      output_dict['detection_boxes'],
      output_dict['detection_classes'],
      output_dict['detection_scores'],
      category_index,
      instance_masks=output_dict.get('detection_masks_reframed', None),
      use_normalized_coordinates=True,
      line_thickness=8)

  display(Image.fromarray(image_np))

#for image_path in TEST_IMAGE_PATHS:
#  show_inference(detection_model, image_path)

keepAlive=True
while(keepAlive):
  show_inference(detection_model, None)

'''
if (capture is None):
  print("No video device available")
  quit()

with tf.io.gfile.GFile('saved_model.pb') as f:
  graph_def = tf.compat.v1.GraphDef()
  graph_def.ParseFromString(f.read())

with tf.Session as sess:
  sess.graph.as_default()
  tf.import_graph_def()

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
        keepAlive=False'''