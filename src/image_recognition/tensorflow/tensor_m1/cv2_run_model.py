import cv2

cvNet = cv2.dnn.readNetFromTensorflow('./tmp/output_graph.pb', './tmp/output.pbtxt')

width = 480
height = 270

img = cv2.imread('_result.jpg')
rows = img.shape[0]
cols = img.shape[1]

cvNet.setInput(cv2.dnn.blobFromImage(img, size=(width, height), swapRB=True, crop=False))
cvOut = cvNet.forward()

for detection in cvOut[0,0,:,:]:
    score = float(detection[2])
    if (score >0.3):
        left = detection[3] * cols
        top = detection[4] * rows
        right = detection[5] * cols
        bottom = detection[6] * rows
        cv2.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (23, 230, 210), thickness=2)
cv2.imshow('img', img)
cv2.waitKey()