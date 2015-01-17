import cv2
import cv2.cv as cv
import numpy as np
img = cv2.imread('roomba.jpg')
img = cv2.medianBlur(img,5)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
circles = cv2.HoughCircles(gray,cv.CV_HOUGH_GRADIENT,1,20,
                              param1=100,param2=60,minRadius=100,maxRadius=0)
circles = np.uint16(np.around(circles))
temp = img
for i in circles[0,:]:
  # draw the outer circle
  cv2.circle(temp,(i[0],i[1]),i[2],(0,255,0),-1)
    # draw the center of the circle
#cv2.circle(temp,(i[0],i[1]),2,(0,0,255),3)
hsv = cv2.cvtColor(temp,cv2.COLOR_BGR2HSV)
lower_green = (55,245,245)
upper_green = (65,255,255)
mask = cv2.inRange(hsv,lower_green,upper_green)
cv2.imshow('circles',mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
