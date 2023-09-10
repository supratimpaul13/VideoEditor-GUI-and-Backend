import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import sys

if len(sys.argv) != 2:
    print("Usage: python your_python_script.py <video_file_path>")
    sys.exit(1)

video_file_path = sys.argv[1]

print(video_file_path + " Working.........")

# cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("test_clip2.mp4")
cap = cv2.VideoCapture(video_file_path)
detector = HandDetector(maxHands=1)
classifier = Classifier(r"C:\Tech Variable\Wireframe\Engine\Model\keras_model.h5", r"C:\Tech Variable\Wireframe\Engine\Model\labels.txt")

offset = 20
imgSize = 300
counter = 0

labels = ["Start", "Pause", "C"]

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

        # cv2.imshow("Image Crop", imgCrop)
        # cv2.imshow("Image White", imgWhite)


    cv2.imshow("Image", imgOutput)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()
