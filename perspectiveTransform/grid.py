import cv2
import numpy as np
from operator import itemgetter, attrgetter, methodcaller
from numpy.linalg import inv
import math


def intersect(p1,p2):
    mat = np.matrix(((math.cos(p1[1]),-math.sin(p1[1])),(math.cos(p2[1]),-math.sin(p2[1]))))
    mat = inv(mat)
    dis = np.matrix((p1[0],p2[0]))
    dis = dis.transpose()
    result = np.dot(mat,dis)
    return result

img = cv2.imread('arena.jpg')
img = cv2.resize(img,(800,600))
img = cv2.medianBlur(img,5)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
cv2.imshow("edges",edges)
#lines = cv2.HoughLines(edges,1,np.pi/180,80)
lines = cv2.HoughLines(edges,1,np.pi/180,100,50,10)
good = []
temp = []
arr1 = []
arr2 = []
hight, width, channel = img.shape
if lines != None:
  for m,n in lines[0]:
      temp.append((m,n))
# sort with distance
  temp.sort(key=lambda elem: elem[0])
  len = len(temp)
  goodlen = 0
# delete multiple overlapping lines
  for x in range(0,len):
    isLine = True
    for y in range(x+1,len):
      if x == y: continue
      if x != len-1:
        if abs(temp[x][0]-temp[y][0]) < 0.05*width:
          if abs(temp[x][1]-temp[y][1]) < 0.25:
              isLine = False
    if isLine:
      good.append([temp[x][0],temp[x][1]])
      goodlen = goodlen + 1
#calculate angle
  print goodlen

  intesecLength = 0
  intesec = []
  for x in range(0,goodlen):
    for y in range(x+1,goodlen):      
      A = good[x]
      B = good[y]
      print intersect(A,B)
      intesec.append(intersect(A,B))
      intesecLength = intesecLength + 1
 
  for x in range(0,intesecLength):
    cv2.circle(img,(int(intesec[x][0,0]),-int(intesec[x][1,0])),10,255,-1)
  
  '''
  if A is not None:
    intesec = intersect(A,B)
    print intesec[0,0]
    cv2.circle(img,(int(intesec[0,0]),-int(intesec[1,0])),10,255,-1)
   '''
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