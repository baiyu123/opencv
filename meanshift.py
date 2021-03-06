import cv2
import numpy as np
<<<<<<< Updated upstream
import cv2.cv as cv
import scipy as sp
import time

original = cv2.imread('roomba.jpg')
cap = cv2.VideoCapture(0)
lower_green = (55,245,245)
upper_green = (65,255,255)
track_window = None


while(1):
    ret, frame = cap.read()
    if ret == True:
      gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
      gray = cv2.GaussianBlur(gray,(9,9),0)
      circles = cv2.HoughCircles(gray,cv.CV_HOUGH_GRADIENT,1,20,
                             param1=120,param2=50,minRadius=20,maxRadius=0)
      view = frame
      if circles != None:
          circles = np.uint16(np.around(circles))
          temp = frame
          start_time = time.time()
          for i in circles[0,:]:
             # draw the outer circle
             cv2.circle(view,(i[0],i[1]),i[2],(0,255,0),3)
             c = i[0]-i[2]
             r = i[1]-i[2]
             w = 2*i[2]
             h = w
            # draw the center of the circle
            #cv2.circle(temp,(i[0],i[1]),2,(0,0,255),3)
          track_window = (c,r,w,h)
          roi = frame[r:r+h,c:c+h]
          hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
          mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
          roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
          cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
          term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
          
          hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
          dst = cv2.calcBackProject([hsv_frame],[0],roi_hist,[0,180],1)
          ret, track_window = cv2.meanShift(dst,track_window,term_crit)
          x,y,w,h = track_window
          cv2.rectangle(frame,(x,y),(x+w,y+h),255,2)
      elif track_window != None:
          hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
          dst = cv2.calcBackProject([hsv_frame],[0],roi_hist,[0,180],1)
          ret, track_window = cv2.meanShift(dst,track_window,term_crit)
          x,y,w,h = track_window
          cv2.rectangle(frame,(x,y),(x+w,y+h),255,2)
          print time.time()-start_time
          if time.time()-start_time > 3:
              track_window = None
      cv2.imshow('view',frame)
      k = cv2.waitKey(60) & 0xff
      if k == 27:
         break
cv2.destroyAllWindows()
cap.release()
=======

frame = cv2.imread('table.jpg')
r,h,c,w = 1000,100,1000,100
track_window = (c,r,w,h)

roi = frame[r:r+h, c:c+w]
hsv_roi =  cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0.,60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

cv2.imshow('view',roi_hist)
cv2.waitKey(0)
cv2.destroyAllWindows()
>>>>>>> Stashed changes
