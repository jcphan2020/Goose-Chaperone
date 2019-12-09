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

capture_id = 1
capture = cv.VideoCapture(capture_id)

# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1

# Patch the location of gfile
tf.gfile = tf.io.gfile

#Important Tags
HUMAN=1
BIRD=16

#Indexes
CLASSES_IDX=0
SCORES_IDX=1
BOX_IDX=2

def load_model(model_dir):
  #Good for pulling fresh models

  #base_url = 'http://download.tensorflow.org/models/object_detection/'
  #model_file = model_name + '.tar.gz'
  #model_dir = tf.keras.utils.get_file(
  #  fname=model_name, 
  #  origin=base_url + model_file,
  #  untar=True)

  #model_dir = pathlib.Path(model_dir)/"saved_model"

  model = tf.saved_model.load(str(model_dir))
  model = model.signatures['serving_default']

  print(">>>>>>>>>>>>>>")
  print(model_dir)

  return model
detection_model = load_model('./')
# List of the strings that is used to add correct label for each box.
#PATH_TO_LABELS = 'models/research/object_detection/data/mscoco_label_map.pbtxt'
PATH_TO_LABELS = './mscoco_label_map.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

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

  return output_dict

def show_inference(model, sess):
  ret,img = capture.read()
  rows = img.shape[0]
  cols = img.shape[1]
  inp = cv.resize(img, (300, 300))
  inp = inp[:, :, [2, 1, 0]]  # BGR2RGB

  image_np = inp
  # Actual detection.
  output_dict = run_inference(model, image_np)

  scores = output_dict['detection_scores']
  classes = output_dict['detection_classes']
  boxes = output_dict['detection_boxes']

  #Get detected object data
  r = []
  i=0
  while i<len(scores):
    if (scores[i] > 0.5):
      r.append((classes[i],scores[i], boxes[i]))
    i=i+1

  return r

def get_detections():
  return show_inference(detection_model, None)

def get_box_area(box):
  c1=box[0]
  c2=box[1]
  c3=box[2]
  c4=box[3]
  return (c2-c1) * (c4-c3)

