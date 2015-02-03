import cv2
import numpy as np
cap = cv2.VideoCapture(0)
while True:
  ret, frame = cap.read()
  #img = cv2.imread('roomba.jpg')
  blur = cv2.GaussianBlur(frame,(9,9),0)
  hsv_img = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
  lower_white = np.array([0,0,70])
  higher_white = np.array([179,50,255])
  mask = cv2.inRange(hsv_img,lower_white,higher_white)
  result = cv2.bitwise_and(frame,frame,mask= mask)
  cv2.imshow('view',result)
  k=cv2.waitKey(1)
  if k==27:
      break
cap.release()
cv2.destroyAllWindows()

