import numpy as np
import cv2
##Specify file path for pic
im = cv2.imread("OnBoard.jpg")
im = cv2.resize(im, (1000,700))

cv2.threshold(im, 250, 255, cv2.THRESH_BINARY, im)
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(im,contours,-1,(0,255,0),3)

cv2.imshow("OnBoard.jpg", im)


cv2.waitKey(0)
cv2.destroyAllWindows()
