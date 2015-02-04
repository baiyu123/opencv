import cv2
import numpy as np

img = cv2.imread('roomba.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)

cv2.imshow('view',sobely)

cv2.waitKey(0)
cv2.destroyAllWindows()
