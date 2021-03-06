import cv2 as cv

dir='./ssd_mobilenet_v1_coco_2018_01_28/'

capture = cv2.VideoCapture(0)
cv2.namedWindow('display')
graph = dir+frozen_inference_graph.pb
width = 480
height = 270
export_jpg = '_info.jpg'
conf_thresh=.3

cvNet = cv.dnn.readNetFromTensorflow(dir+'frozen_inference_graph.pb', dir+'model.pbtxt')

img = cv.imread('horse.jpg')
rows = img.shape[0]
cols = img.shape[1]
cvNet.setInput(cv.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False))
cvOut = cvNet.forward()

for detection in cvOut[0,0,:,:]:
    score = float(detection[2])
    if score > 0.3:
        left = detection[3] * cols
        top = detection[4] * rows
        right = detection[5] * cols
        bottom = detection[6] * rows
        cv.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (23, 230, 210), thickness=2)

cv.imshow('img', img)
cv.waitKey()