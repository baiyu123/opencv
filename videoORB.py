import numpy as np
import cv2
import cv2.cv as cv
import scipy as sp
from matplotlib import pyplot as plt
import time

cap = cv2.VideoCapture(0)
original = cv2.imread('croproomba.jpg')
original = cv2.resize(original,(600,800))
orb = cv2.ORB()
kp1, des1 = orb.detectAndCompute(original,None)

FLANN_INDEX_LSH = 1
index_params = dict(algorithm = FLANN_INDEX_LSH,
                    table_number = 6,
                    key_size = 12,
                    multi_probe_level = 1)
search_params = dict(checks=100)
lower_green = (55,245,245)
upper_green = (65,255,255)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.resize(frame,(800,600))
    #masking
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray,cv.CV_HOUGH_GRADIENT,1,20,
                           param1=100,param2=60,minRadius=0,maxRadius=0)
    h1, w1 = original.shape[:2]
    h2, w2 = frame.shape[:2]
    view = sp.zeros((max(h1,h2),w1 + w2, 3), sp.uint8)
    view[:h1, :w1, 0] = original[:, :, 0]
    view[:h2, w1:, 0] = frame[:, :, 0]
    view[:h1, :w1, 1] = original[:, :, 1]
    view[:h2, w1:, 1] = frame[:, :, 1]
    view[:h1, :w1, 2] = original[:, :, 2]
    view[:h2, w1:, 2] = frame[:, :, 2]
    if circles != None:
        circles = np.uint16(np.around(circles))
        temp = frame
        for i in circles[0,:]:
           # draw the outer circle
           cv2.circle(temp,(i[0],i[1]),i[2],(0,255,0),-1)
          # draw the center of the circle
          #cv2.circle(temp,(i[0],i[1]),2,(0,0,255),3)
        hsv = cv2.cvtColor(temp,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv,lower_green,upper_green)
        kp2, des2 = orb.detectAndCompute(frame,mask)

        flann = cv2.FlannBasedMatcher(index_params,search_params)
        matches = flann.knnMatch(des1,des2,k=2)
        print matches
        good = np.array([])
        veryGood = np.array([])
        for m,n in matches:
          if m.distance < 0.7*n.distance:
            good = np.append(good,m)
        min = 99999999
        for m in good:
          if m.distance < min:
              min = m.distance
        for m in good:
          if m.distance < 3*min:
              veryGood = np.append(veryGood,m)



        for m in veryGood:
            color = tuple([sp.random.randint(0,255) for _ in xrange(3)])
            cv2.line(view, (int(kp1[m.queryIdx].pt[0]), int(kp1[m.queryIdx].pt[1])),(int(kp2[m.trainIdx].pt[0]+w1), int(kp2[m.trainIdx].pt[1])),color)
            cv2.circle(view,(int(kp1[m.queryIdx].pt[0]),int(kp1[m.queryIdx].pt[1])),10,255,-1)
            cv2.circle(view,(int(kp2[m.trainIdx].pt[0]+w1), int(kp2[m.trainIdx].pt[1])),10,255,-1)
    cv2.imshow('test',view)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
