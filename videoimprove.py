import numpy as np
import cv2
import cv2.cv as cv
import scipy as sp
from matplotlib import pyplot as plt
import time

#creating mask for original image
lower_white = np.array([0,0,50])
lower_white2 = np.array([0,0,100])
higher_white = np.array([179,50,255])

#loading the target image
cap = cv2.VideoCapture(0)
lower_green = (55,245,245)
upper_green = (65,255,255)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    #frame = cv2.imread('roombafar.jpg')
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
          count = 0;
          for i in circles[0,:]:
             # draw the outer circle
             #cv2.circle(temp,(i[0],i[1]),i[2],(0,255,0),-1)
             #cv2.circle(view,(i[0],i[1]),i[2],(0,255,0),3)
              cv2.rectangle(temp,(i[0]-i[2],i[1]-i[2]),(i[0]+i[2],i[1]+i[2]),(0,255,0),-1)
              count = count + 1
              if count == 10:
                 break
            # draw the center of the circle
            #cv2.circle(temp,(i[0],i[1]),2,(0,0,255),3)
          hsv = cv2.cvtColor(temp,cv2.COLOR_BGR2HSV)
          mask = cv2.inRange(hsv,lower_green,upper_green)
          result = cv2.bitwise_and(frame,frame,mask= mask)
          hsv_result = cv2.cvtColor(result,cv2.COLOR_BGR2HSV)
          bimask = cv2.inRange(hsv_result,lower_white2,higher_white)
          bimaskblur = cv2.GaussianBlur(bimask,(7,7),0)
          #2nd = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
          cv2.imshow('result',bimaskblur)
          circles2 = cv2.HoughCircles(bimaskblur,cv.CV_HOUGH_GRADIENT,1,20,
                             param1=120,param2=50,minRadius=20,maxRadius=0)
          if circles2 != None:
             count = 0
             for i in circles[0,:]:
                # draw the outer circle
                #cv2.circle(temp,(i[0],i[1]),i[2],(0,255,0),-1)
                cv2.circle(view,(i[0],i[1]),i[2],(0,255,0),3)
                count = count +1
                if count == 10:
                    break
                  




    cv2.imshow('test',view)
    if cv2.waitKey(1) & 0xFF == ord('q'):
          break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
