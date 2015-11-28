import cv2
import numpy as np

img = cv2.imread("grid2.jpg")

pts1 = np.float32([[148,166],[354,162],[96,282],[499,256]])
pts2 = np.float32([[300,300],[400,300],[300,400],[400,400]])

M = cv2.getPerspectiveTransform(pts1,pts2)
print M
dst = cv2.warpPerspective(img,M,(600,600))

cv2.imshow("original",img)
cv2.imshow('transformed',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()