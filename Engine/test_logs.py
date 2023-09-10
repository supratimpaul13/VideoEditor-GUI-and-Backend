import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import time
import math

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("test_clip2.mp4")
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

offset = 20
imgSize = 300
counter = 0

labels = ["Start", "Pause", "C"]


start_time = None
start_count = 0
continuous_time_threshold = 5  # 3 seconds

while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    # cv2.waitKey(1)

    if hands:
        hand = hands[0]  # as we have only one hand

        # extracting the dimensions of the hands from the bounding box
        x, y, w, h = hand['bbox']

        imgWhite =np.ones((imgSize, imgSize, 3), np.uint8)*255
        imgCrop = img[y-offset:y + h+offset, x-offset:x + w+offset]  # cropping the image

        imgCropShape = imgCrop.shape


        # Bringing the image to the centre of the white imgCrop
        aspectRatio = h/w

        if aspectRatio > 1:
            k = imgSize/h
            wCal = math.ceil(k*w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize-wCal)/2)
            # imgWhite[0:imgResizeShape, 0:imgResizeShape[1]] = imgResize
            imgWhite[:, wGap:wCal+wGap] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)

        else:
            k = imgSize/h
            hCal = math.ceil(k*h)
            imgResize = cv2.resize(imgCrop, (hCal, imgSize))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize-hCal)/2)
            # imgWhite[0:imgResizeShape, 0:imgResizeShape[1]] = imgResize
            imgWhite[:, hGap:hCal+hGap] = imgResize
            prediction, index = classifier.getPrediction(imgWhite)
        

        cv2.rectangle(imgOutput, (x - offset, y - offset - 50), (x - offset + 140, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOutput, labels[index], (x, y-26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
        cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w+offset, y + h+offset), (255, 0, 255), 4)

        if labels[index] == "Start":
            if start_time is None:
                start_time = time.time()
            else:
                elapsed_time = time.time() - start_time
                if elapsed_time >= continuous_time_threshold:
                    start_count += 1
                    if start_count >= 5:
                        with open("output.txt", "a") as file:
                            file.write("Start\n")
                        start_count = 0
                        start_time = None

        elif labels[index] == "Pause":
            if start_time is None:
                start_time = time.time()
            else:
                elapsed_time = time.time() - start_time
                if elapsed_time >= continuous_time_threshold:
                    start_count += 1
                    if start_count >= 5:
                        with open("output.txt", "a") as file:
                            file.write("Pause\n")
                        start_count = 0
                        start_time = None

        else:
            start_time = None
            start_count = 0


        # cv2.imshow("Image Crop", imgCrop)
        # cv2.imshow("Image White", imgWhite)


    cv2.imshow("Image", imgOutput)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()
