import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0)

def findMaxContour(contours):
    max_i = 0
    max_area = 0

    for i in range(len(contours)):
        area_face = cv2.contourArea(contours[i])
        if max_area < area_face:
            max_area = area_face
            max_i = i
        try:
            c = contours[max_i]
        except:
            contours = [0]
            c = contours[0]

        return c

while 1:
    ret , frame = cap.read()
    frame = cv2.flip(frame , 1)
    roi = frame[50:250 , 200:400]
    cv2.rectangle(frame , (200 , 50) , (400 , 250) , (0,0,255) , 0)

    hsv = cv2.cvtColor(roi , cv2.COLOR_BGR2HSV)
    lower_color = np.array([0,45,79],dtype=np.uint8)
    upper_color = np.array([17,255,255],dtype=np.uint8)

    mask = cv2.inRange(hsv , lower_color , upper_color)
    kernel = np.ones((3,3) , np.uint8)
    mask = cv2.dilate(mask , kernel , iterations=1)
    mask = cv2.medianBlur(mask , 15)

    contours , _ = cv2.findContours(mask , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        try:
            c = findMaxContour(contours)
            extremeLeft = tuple(c[c[: , : , 0].argmin()][0])
            extremeRight = tuple(c[c[: , : , 0].argmax()][0])
            extremeTop = tuple(c[c[: , : , 1].argmin()][0])
            extremeBot = tuple(c[c[: , : , 1].argmax()][0])

            cv2.circle(roi , extremeLeft , 5 , (0,255,0) , 2)
            cv2.circle(roi , extremeRight , 5 , (0,255,0) , 2)
            cv2.circle(roi , extremeTop , 5 , (0,255,0) , 2)
            cv2.circle(roi , extremeBot , 5 , (0,255,0) , 2)

            cv2.line(roi , extremeLeft , extremeTop , (255,0,0) , 2)
            cv2.line(roi, extremeTop, extremeRight, (255, 0, 0), 2)
            cv2.line(roi, extremeRight, extremeBot, (255, 0, 0), 2)
            cv2.line(roi, extremeBot, extremeLeft, (255, 0, 0), 2)

            a = math.sqrt((extremeRight[0] - extremeTop[0])**2 + (extremeRight[1] - extremeTop[1])**2)
            b = math.sqrt((extremeBot[0] - extremeRight[0])**2 + (extremeBot[1] - extremeRight[1])**2)
            c = math.sqrt((extremeBot[0] - extremeTop[0])**2 + (extremeBot[1] - extremeTop[1])**2)

            try:
                angle_ab = int(math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * b * c)) * 57)
                cv2.putText(roi , str(angle_ab) , (extremeRight[0]-100 , extremeRight[1]) , cv2.FONT_HERSHEY_SIMPLEX , 2 ,  (0,0,255)
                            ,cv2.LINE_AA)
            except:
                cv2.putText(roi, "?", (extremeRight[0] - 100, extremeRight[1]), cv2.FONT_HERSHEY_SIMPLEX, 2,
                            (0, 0, 255), cv2.LINE_AA)

        except:
            pass

    else:
        pass

    cv2.imshow("frame" , frame)
    cv2.imshow("roi" , roi)
    cv2.imshow("Mask" , mask)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()