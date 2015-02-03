import cv2
import numpy as np
import cv2.cv as cv
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
while(1):
  ret, target = cap.read()
  #target = cv2.imread('roombao.jpg')
  hsvt = cv2.cvtColor(target,cv2.COLOR_BGR2HSV)
  #calculating backprojection
  dst = cv2.calcBackProject([hsvt],[0,1],roihist,[0,180,0,256],1)
  disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
  cv2.filter2D(dst,-1,disc,dst)
  ret,thresh = cv2.threshold(dst,50,255,0)
  thresh = cv2.merge((thresh,thresh,thresh))
  thresh = cv2.blur(thresh,(9,9))
  res = cv2.bitwise_and(target,thresh)
  k = cv2.waitKey(1)
  gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
  gray = cv2.GaussianBlur(gray,(9,9),0)
  circles = cv2.HoughCircles(gray,cv.CV_HOUGH_GRADIENT,1,20,
                             param1=120,param2=50,minRadius=20,maxRadius=0)
  if circles != None:
     circles = np.uint16(np.around(circles))
     count = 0
     for i in circles[0,:]:
         # draw the outer circle
         cv2.circle(target,(i[0],i[1]),i[2],(0,255,0),3)
         count = count+1
         if count == 10:
            break
  cv2.imshow('view',target)
  cv2.imshow('thresh',thresh)
  if k == 27:
      break
cap.release()
cv2.destroyAllWindows()
