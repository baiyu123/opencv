import cv2
import numpy as np
img = cv2.imread('croproomba.jpg')
circles = cv2.HoughCircles(img,CV_HOUGH_GRADIENT,1,20,
                              param1=50,param2=30,minRadius=0,maxRadius=0)
print circles
