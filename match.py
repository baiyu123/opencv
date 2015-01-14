import cv2
import numpy as np
import scipy as sp
from matplotlib import pyplot as plt
original = cv2.imread('original.jpg')
match = cv2.imread('side.jpg')
orb = cv2.ORB()
kp1, des1 = orb.detectAndCompute(original,None)
kp2, des2 = orb.detectAndCompute(match,None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
matches = bf.match(des1,des2)
#matches = sorted(matches, key = lambda x:x.distance)

good = []
x = 1
len = len(matches)

for m in matches:
  if x < len:
    n = matches[x]
    x = x + 1
    if m.distance < 0.7*n.distance:
      good.append(m)

h1, w1 = original.shape[:2]
h2, w2 = match.shape[:2]
view = sp.zeros((max(h1,h2),w1 + w2, 3), sp.uint8)
view[:h1, :w1, 0] = original[:, :, 2]
view[:h2, w1:, 0] = match[:, :, 2]
view[:h1, :w1, 1] = original[:, :, 1]
view[:h2, w1:, 1] = match[:, :, 1]
view[:h1, :w1, 2] = original[:, :, 0]
view[:h2, w1:, 2] = match[:, :, 0]


for m in good:
    color = tuple([sp.random.randint(0,255) for _ in xrange(3)])
    cv2.line(view, (int(kp1[m.queryIdx].pt[0]), int(kp1[m.queryIdx].pt[1])),(int(kp2[m.trainIdx].pt[0]+w1), int(kp2[m.trainIdx].pt[1])),color)
    cv2.circle(view,(int(kp1[m.queryIdx].pt[0]),int(kp1[m.queryIdx].pt[1])),10,255,-1)
    cv2.circle(view,(int(kp2[m.trainIdx].pt[0]+w1), int(kp2[m.trainIdx].pt[1])),10,255,-1)


plt.imshow(view),plt.show()