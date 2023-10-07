import math
import mediapipe as mp
import numpy as np
import cv2.cv2 as cv

mp_drawing = mp.solutions.drawing_utils

mp_hands = mp.solutions.hands
tipIds = [4,8,12,16,20]
def Hand_land_marks(image,hands):
    image.flags.writeable = False
    result = hands.process(image)
    image.flags.writeable = True


    print(result)
    if result.multi_hand_landmarks:
        for num, hand in enumerate(result.multi_hand_landmarks):
            mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)



def findPosition(image,hands, handNo=0, draw=True):
   
    xList = []
   
    yList = []
    
    bbox = []
    
    lmList = []

    result = hands.process(image)

    if result.multi_hand_landmarks:
        myHand = result.multi_hand_landmarks[handNo]
	

        for id , lm in enumerate(myHand.landmark):

            h,w,c=image.shape

            cx,cy = int(lm.x*w),int(lm.y*h)

            xList.append(cx)

            yList.append(cy)

            lmList.append([id,cx,cy])

            if draw:

                cv.circle(image,(cx,cy),5,(155,0,155),cv.FILLED)

        xmin,xmax = min(xList),max(xList)

        ymin,ymax = min(yList),max(yList)

        bbox = xmin,ymin,xmax,ymax

        if draw:


            cv.rectangle(image,(xmin - 20, ymin - 20), (xmax + 20, ymax + 20),(0, 255, 0), 2)

        return lmList


def fingerup(lmList):

    fingers = []

    if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:

        fingers.append(1)

    else:

        fingers.append(0)

    for id in range(1,5):

        if lmList[tipIds[id]][2]  < lmList[tipIds[id]-2][2]:

            fingers.append(1)

        else:

            fingers.append(0)

    return fingers


def findDistance(lmList,p1 , p2 , image , draw = True , r =15 ,t=3):

    x1,y1 = lmList[p1][1:]

    x2, y2 = lmList[p2][1:]

    cx , cy = (x1+x2)//2,(y1+y2)//2

    if draw:
        cv.line(image,(x1,y1),(x2,y2),(255,0,255),t)
        cv.circle(image,(x1,y1),r,(255,0,255),cv.FILLED)

        cv.circle(image,(x2,y2),r,(255,0,255),cv.FILLED)

        cv.circle(image, (cx,cy), r, (0, 0, 255), cv.FILLED)
    length = math.hypot(x2 - x1 , y2 - y1)
    return length , image,[x1,y1,x2,y2,cx,cy]











