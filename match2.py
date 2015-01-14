import cv2
import numpy as np
import scipy as sp
from matplotlib import pyplot as plt
original = cv2.imread('keyboard.jpg')
match = cv2.imread('table.jpg')
sift = cv2.SIFT()
kp1, des1 = sift.detectAndCompute(original,None)
kp2, des2 = sift.detectAndCompute(match,None)
"""
bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck = True)
matches = bf.knnMatch(des1,des2,2)
#matches = sorted(matches, key = lambda x:x.distance)


"""
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary

flann = cv2.FlannBasedMatcher(index_params,search_params)

matches = flann.knnMatch(des1,des2,k=2)
good = []


for m,n in matches:
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