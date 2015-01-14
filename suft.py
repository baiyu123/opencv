import cv2
import numpy as np
img = cv2.imread('dorm.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
suft = cv2.SIFT(500)
kp,des = suft.detectAndCompute(img,None)
img = cv2.drawKeypoints(gray,kp,None,(255,0,0),10)
print len(kp)
cv2.imshow('test',img)
cv2.waitKey(0)
cv2.destroyAllWindows()