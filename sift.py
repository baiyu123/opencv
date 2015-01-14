import cv2
import numpy as np
img = cv2.imread('dorm.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
sift = cv2.SIFT()
kp = sift.detect(gray,None)
"""
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv,lower_blue,upper_blue)
"""
kp,des = sift.compute(gray,kp)
img = cv2.drawKeypoints(gray,kp)
print len(kp)
cv2.imshow('test',img)
cv2.waitKey(0)
cv2.destroyAllWindows()