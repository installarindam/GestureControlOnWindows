import cv2
import mediapipe as mp
import time
import HandtrackingModule as hmt

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = hmt.handDetector()
while True:
    success, img = cap.read()
    img = detector.findHands(img)  #(img, draw=True/False)
    lmList = detector.findPosition(img) #(img, draw=True/False)
    if len(lmList) != 0:
        print(lmList[4])
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    # position           #scale#colorcodein rgb #thickness

    cv2.imshow("Image", img)
    cv2.waitKey(1)
