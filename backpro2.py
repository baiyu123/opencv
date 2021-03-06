import numpy as np
import cv2
import cv2.cv as cv
import scipy as sp
from matplotlib import pyplot as plt
import time

#creating mask for original image
original = cv2.imread('roomba.jpg')
blurO = cv2.GaussianBlur(original,(9,9),0)
hsv_o = cv2.cvtColor(blurO,cv2.COLOR_BGR2HSV)
lower_white = np.array([0,0,50])
higher_white = np.array([179,50,255])
mask = cv2.inRange(hsv_o,lower_white,higher_white)
#creating histogram for original image
hsv = cv2.cvtColor(original,cv2.COLOR_BGR2HSV)
roihist = cv2.calcHist([hsv],[0, 1], mask, [180, 256], [0, 180, 0, 256] )
cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)
#loading the target image
cap = cv2.VideoCapture(0)
lower_green = (55,245,245)
upper_green = (65,255,255)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
#      frame = cv2.resize(frame,(800,600))
      #masking
      gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
      gray = cv2.GaussianBlur(gray,(9,9),0)
      circles = cv2.HoughCircles(gray,cv.CV_HOUGH_GRADIENT,1,20,
                             param1=120,param2=50,minRadius=20,maxRadius=0)

      #h2, w2 = frame.shape[:2]
      view = frame.copy()
      temp = frame.copy()
      if circles != None:
          circles = np.uint16(np.around(circles))
          for i in circles[0,:]:
             # draw the outer circle
             cv2.circle(temp,(i[0],i[1]),i[2],(0,255,0),-1)
             cv2.circle(view,(i[0],i[1]),i[2],(0,255,0),3)
            # draw the center of the circle
            #cv2.circle(temp,(i[0],i[1]),2,(0,0,255),3)

          hsv = cv2.cvtColor(temp,cv2.COLOR_BGR2HSV)
          mask = cv2.inRange(hsv,lower_green,upper_green)
          result = cv2.bitwise_and(frame,frame,mask= mask)
          hsvt = cv2.cvtColor(result,cv2.COLOR_BGR2HSV)
          #calculating backprojection
          dst = cv2.calcBackProject([hsvt],[0,1],roihist,[0,180,0,256],1)
          disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
          cv2.filter2D(dst,-1,disc,dst)
          ret,thresh = cv2.threshold(dst,50,0,cv2.THRESH_BINARY)
          thresh = cv2.merge((thresh,thresh,thresh))
          thresh = cv2.blur(thresh,(9,9))
          res = cv2.bitwise_and(frame,thresh)
          cv2.imshow('res',thresh)



    cv2.imshow('test',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
          break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
