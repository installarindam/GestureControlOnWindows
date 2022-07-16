import cv2
import time
import os

import HandtrackingModule as htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderpath = "fingers"
myList = os.listdir(folderpath)
print(myList)
pTime = 0
overlayList = []


for imPath in myList:
    image = cv2.imread(f'{folderpath}/{imPath}')
    overlayList.append(image)

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

while True:

    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)

    if len(lmList) != 0:
        fingers = []

        # thumb (use right hand)
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # another 4 finger
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)


        h, w, c = overlayList[totalFingers - 1].shape
        # image size 200X200 recomended
        img[0:h, 0:w] = overlayList[totalFingers - 1]

        cv2.rectangle(img, (28, 255), (178, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    cv2.imshow("Images", img)
    cv2.waitKey(1)
