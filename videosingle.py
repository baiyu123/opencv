import numpy as np
import cv2
import scipy as sp
from matplotlib import pyplot as plt

frame = cv2.imread('side.jpg')
original = cv2.imread('croproomba.jpg')
original = cv2.resize(original,(600,800))
surf = cv2.SURF(400)
kp1, des1 = surf.detectAndCompute(original,None)
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)


frame = cv2.resize(frame,(800,600))
kp2, des2 = surf.detectAndCompute(frame,None)
flann = cv2.FlannBasedMatcher(index_params,search_params)
matches = flann.knnMatch(des1,des2,k=2)
good = np.array([])
veryGood = np.array([])
for m,n in matches:
  if m.distance < 0.7*n.distance:
    good = np.append(good,m)
min = 99999999
for m in good:
  if m.distance < min:
     min = m.distance
print min
for m in good:
  if m.distance < 2*min:
      veryGood = np.append(veryGood,m)
h1, w1 = original.shape[:2]
h2, w2 = frame.shape[:2]
view = sp.zeros((max(h1,h2),w1 + w2, 3), sp.uint8)
view[:h1, :w1, 0] = original[:, :, 0]
view[:h2, w1:, 0] = frame[:, :, 0]
view[:h1, :w1, 1] = original[:, :, 1]
view[:h2, w1:, 1] = frame[:, :, 1]
view[:h1, :w1, 2] = original[:, :, 2]
view[:h2, w1:, 2] = frame[:, :, 2]
    
if veryGood.size > 10:
  for m in veryGood:
    color = tuple([sp.random.randint(0,255) for _ in xrange(3)])
    cv2.line(view, (int(kp1[m.queryIdx].pt[0]), int(kp1[m.queryIdx].pt[1])),(int(kp2[m.trainIdx].pt[0]+w1), int(kp2[m.trainIdx].pt[1])),color)
    cv2.circle(view,(int(kp1[m.queryIdx].pt[0]),int(kp1[m.queryIdx].pt[1])),10,255,-1)
    cv2.circle(view,(int(kp2[m.trainIdx].pt[0]+w1), int(kp2[m.trainIdx].pt[1])),10,255,-1)
  
cv2.imshow('test',view)
if cv2.waitKey(0) & 0xFF == ord('q'):
  cv2.destroyAllWindows()