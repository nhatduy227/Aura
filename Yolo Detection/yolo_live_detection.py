from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import threading
import cv2
import imutils
from pathlib import Path
import numpy as np

# constants
base_path = Path(__file__).parent
weights_path = str(base_path) + "\pretrained models\yolov3.weights"
cfg_path = str(base_path) + "\pretrained models\yolov3.cfg"
coco_path = str(base_path) + "\pretrained models\coco.names"
font = cv2.FONT_HERSHEY_PLAIN

# Load Yolo
net = cv2.dnn.readNet(weights_path, cfg_path)
classes = []  # loading all the object classes from coco.names to the classes variable
with open(coco_path, "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

#image_processing_functions
def process_frame(frame): 
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)
    return outs

def show_detected_object(outs): 
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y + 30), font, 3, color, 3)

# Camera Rendering
cap = WebcamVideoStream(src=0).start() 

while True: 
    # Start FPS counter
    fps = FPS().start()

    # loading frame
    frame = cap.read()
    frame = cv2.resize(frame, None, fx=1.5, fy=1.5,
                       interpolation=cv2.INTER_AREA)
    height, width, channels = frame.shape

    # Detecting objects
    output = process_frame(frame)
    show_detected_object(output)

    fps.update()
    fps.stop()
    if (fps._end - fps._start).total_seconds() != 0: 
        cv2.putText(frame, "FPS: "+ str(round(fps.fps(),2)), (30, 40), font, 3, (255, 0, 0), 3)

    cv2.imshow('LiveStream', frame)
    c = cv2.waitKey(1)  # Destroy window on Exit pressed
    if c == 27:
        break

cap.stop()
cv2.destroyAllWindows()
