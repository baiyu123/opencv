import cv2
import numpy as np
from operator import itemgetter, attrgetter, methodcaller
img = cv2.imread('grid.jpg')
img = cv2.medianBlur(img,5)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#th = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
lines = cv2.HoughLines(edges,1,np.pi/180,200)
good = []
temp = []
arr1 = []
arr2 = []

hight, width, channel = img.shape
for m,n in lines[0]:
    temp.append((m,n))

temp.sort(key=lambda elem: elem[0])
print temp[0][0]
len = len(temp)
print lines
for x in range(0,len-1):
  if abs(temp[x+1][0]-temp[x][0]) > 0.1*width:
        good.append([temp[x][0],temp[x][1]])
        good.append([temp[x+1][0],temp[x+1][1]])
        x = x+1
  elif abs(temp[x+1][1]-temp[x][1]) > 0.55:
        good.append([temp[x][0],temp[x][1]])
        good.append([temp[x+1][0],temp[x+1][1]])
        x = x+1

print good
for rho,theta in good:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    
    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
cv2.imshow('grid',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
