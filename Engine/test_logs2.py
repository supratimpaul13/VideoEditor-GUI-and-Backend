# import cv2
# from cvzone.HandTrackingModule import HandDetector
# from cvzone.ClassificationModule import Classifier
# import numpy as np
# import math
# import time

# cap = cv2.VideoCapture("test_clip2.mp4")
# detector = HandDetector(maxHands=1)
# classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

# offset = 20
# imgSize = 300
# counter = 0

# labels = ["Start", "Pause", "C"]

# start_prediction_time = None
# pause_prediction_time = None

# start_threshold = 5  # 5 seconds
# pause_threshold = 5  # 5 seconds

# output_file = open("output.txt", "a")  # Open the text file in append mode

# while True:
#     success, img = cap.read()
#     imgOutput = img.copy()
#     hands, img = detector.findHands(img)

#     if hands:
#         hand = hands[0]

#         x, y, w, h = hand['bbox']
#         imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
#         imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
#         imgCropShape = imgCrop.shape

#         aspectRatio = h / w

#         if aspectRatio > 1:
#             k = imgSize / h
#             wCal = math.ceil(k * w)
#             imgResize = cv2.resize(imgCrop, (wCal, imgSize))
#             imgResizeShape = imgResize.shape
#             wGap = math.ceil((imgSize - wCal) / 2)
#             imgWhite[:, wGap:wCal + wGap] = imgResize
#             prediction, index = classifier.getPrediction(imgWhite, draw=False)

#         else:
#             k = imgSize / h
#             hCal = math.ceil(k * h)
#             imgResize = cv2.resize(imgCrop, (hCal, imgSize))
#             imgResizeShape = imgResize.shape
#             hGap = math.ceil((imgSize - hCal) / 2)
#             imgWhite[:, hGap:hCal + hGap] = imgResize
#             prediction, index = classifier.getPrediction(imgWhite)

#         cv2.rectangle(imgOutput, (x - offset, y - offset - 50), (x - offset + 140, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
#         cv2.putText(imgOutput, labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
#         cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (255, 0, 255), 4)

#         current_time = time.time()

#         if labels[index] == "Start":
#             if start_prediction_time is None:
#                 start_prediction_time = current_time
#             elif current_time - start_prediction_time >= start_threshold:
#                 start_prediction_time = None
#                 output_file.write(f"Start - {current_time:.2f}\n")
#                 output_file.flush()  # Flush the buffer to make sure data is written to the file

#             pause_prediction_time = None

#         elif labels[index] == "Pause":
#             if pause_prediction_time is None:
#                 pause_prediction_time = current_time
#             elif current_time - pause_prediction_time >= pause_threshold:
#                 pause_prediction_time = None
#                 output_file.write(f"Pause - {current_time:.2f}\n")
#                 output_file.flush()

#             start_prediction_time = None

#     cv2.imshow("Image", imgOutput)

#     key = cv2.waitKey(1)
#     if key & 0xFF == ord('q'):
#         break

# cap.release()
# output_file.close()  # Close the output file
# cv2.destroyAllWindows()

import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import time

cap = cv2.VideoCapture(0);
# cap = cv2.VideoCapture("test_clip2.mp4")
frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

offset = 20
imgSize = 300
counter = 0

labels = ["Start", "Pause", "C"]

start_prediction_time = None
pause_prediction_time = None

start_threshold = 4  # 5 seconds
pause_threshold = 4  # 5 seconds

output_file = open("output.txt", "a")  # Open the text file in append mode

while True:
    success, img = cap.read()
    if not success:
        break
    
    imgOutput = img.copy()
    hands, img = detector.findHands(img)

    frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    current_time = frame_number / frame_rate

    if hands:
        hand = hands[0]

        x, y, w, h = hand['bbox']
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
        imgCropShape = imgCrop.shape

        aspectRatio = h / w

        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)

        else:
            k = imgSize / h
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (hCal, imgSize))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[:, hGap:hCal + hGap] = imgResize
            prediction, index = classifier.getPrediction(imgWhite)

        cv2.rectangle(imgOutput, (x - offset, y - offset - 50), (x - offset + 140, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOutput, labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
        cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (255, 0, 255), 4)

        if labels[index] == "Start":
            if start_prediction_time is None:
                start_prediction_time = current_time
            elif current_time - start_prediction_time >= start_threshold:
                start_prediction_time = None
                output_file.write(f"Start - {current_time:.2f}\n")
                output_file.flush()

            pause_prediction_time = None

        elif labels[index] == "Pause":
            if pause_prediction_time is None:
                pause_prediction_time = current_time
            elif current_time - pause_prediction_time >= pause_threshold:
                pause_prediction_time = None
                output_file.write(f"Pause - {current_time:.2f}\n")
                output_file.flush()

            start_prediction_time = None

    cv2.imshow("Image", imgOutput)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

cap.release()
output_file.close()  # Close the output file
cv2.destroyAllWindows()


