import numpy as np
import handMarking as hm
import cv2.cv2 as cv
import mediapipe as mp
import autopy
import pyautogui as pag


wCam , hCam = 640,480

frameR = 100

smoothening = 7

pTime = 0

plocX, plocY=0, 0
clocX, clocY=0,0
mp_hands = mp.solutions.hands


cap = cv.VideoCapture(0)

cap.set(3, wCam)

cap.set(4,hCam)

wScr , hScr = autopy.screen.size()

lmlist = []


with mp_hands.Hands(min_detection_confidence=0.8,
 min_tracking_confidence=0.5, max_num_hands=1) as hands:
    while cap.isOpened():

       sucess, frame = cap.read()

       image = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

       #step-1 to mark hand land marks

       hm.Hand_land_marks(image,hands)
       lmlist = hm.findPosition(image,hands)


       try:
        if len(lmlist) != 0:

            x1,y1 = lmlist[8][1:]

            x2,y2 = lmlist[12][1:]

        else :

            pass

        fingers = hm.fingerup(lmlist)

        cv.rectangle(image,(frameR,frameR),(wCam-
frameR,hCam-frameR),(255,0,255),2)

       except:

           pass

       try:

        if fingers[1] == 1 and fingers[2]==0:

            x3 = np.interp(x1,(frameR,wCam-frameR),(0,wScr))

            y3 = np.interp(y1, (frameR,hCam-frameR),(0,hScr))

            clocX = plocX + (x3-plocX) / smoothening

            clocY = plocY + (y3-plocY)/smoothening


            autopy.mouse.move(wScr-clocX,clocY)

            cv.circle(image,(x1,y1),15,(255,0,255),cv.FILLED)

            plocX,plocY = clocX,clocY

       except:

           pass
       try:
           if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0:
            length,image,lineInfo = hm.findDistance(lmlist,8,12,image)
            print(length)

           if length <40:
                cv.circle(image,(lineInfo[4],lineInfo[5]),15,(0,255,0),cv.FILLED)

                pag.click(button='left', clicks=3, interval=0.25)

       except:

           pass
       try:
        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1:
            length,image,lineInfo = hm.findDistance(lmlist,8,12,image)
            print(length)
            if length<40:
                cv.circle(image,(lineInfo[4],lineInfo[5]),15,(0,225,0),cv.FILLED)

                pag.click(button='right', clicks=3, interval=0.25)

       except:

           pass



       cv.imshow("Ai mouse",image)

       cv.waitKey(1)
