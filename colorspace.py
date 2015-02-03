import cv2
import numpy as np

white = np.uint8([[[207,198,189]]])
white = cv2.resize(white,(100,100))
hsv_white = cv2.cvtColor(white,cv2.COLOR_BGR2HSV)
print hsv_white
cv2.imshow('view',white)
cv2.waitKey()
cv2.destroyAllWindows()
