import cv2
import numpy as np

img = cv2.imread('rotateroomba.jpg')
HSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
sobelx = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=5)
sobely = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=5)
xsum = 0
ysum = 0
print sobely
for m in range(134,444):
  for n in range(217,438):
    xsum = xsum + sobelx[m,n]
for m in range(134,444):
  for n in range(217,438):
    ysum = ysum + sobely[m,n]
print xsum
print ysum

if(ysum < 0 and xsum < 0):
  print str('if')
  slope = ysum/xsum
elif(ysum < 0):
  print str('y')
  ysum = abs(ysum)
  slope = ysum/xsum
elif(xsum < 0):
  print str('x')
  xsum = abs(xsum)
  slope = ysum/xsum
else:
  print str('else')
  slope = ysum/xsum
print slope


cv2.imshow('view',gray[134:444,217:438])
cv2.imshow('x',sobelx[134:444,217:438])
cv2.imshow('y',sobely[134:444,217:438])

#cv2.imwrite('map.jpg',sobelx)
cv2.waitKey(0)
cv2.destroyAllWindows()
