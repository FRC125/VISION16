import cv2
from v16Parent import *

#Read and resize the two images

#edit param to include path to image (TRY RESIZE WITH 1280, 720)
img = resize(cv2.imread("Pics/DocExport1/8_15.png"),1000,700)


#Thresh using the Low and High limits and remove noise
initialMask = bit_color(img, LOW_GREEN, HIGH_GREEN)

#Draw the corners onto the image
corners = drawCorners(initialMask,img)

#Show the image
cv2.imshow("im", img)
OrderInitCorners = order_points(np.array(corners))

LeftHeight, RightHeight = getHeightLeftRight(OrderInitCorners)
avgHeight = (LeftHeight+RightHeight)/2
slope = getSlope(OrderInitCorners)
width = getWidth(OrderInitCorners)
aspectRatio = getAspectRatio(avgHeight, width)
theta = getAngle(aspectRatio)
offsetAngle = getOffsetAngle(OrderInitCorners)
distance = getDistance(OrderInitCorners)
offsetDistance = getOffsetDistance(theta,distance) 

print("Distance From Target",distance)
print("Angle Between Robot and Target",theta)
print("Offset Angle", offsetAngle)
print("Offset Horizontal Distance", offsetDistance)

cv2.waitKey(0)
cv2.destroyAllWindows()
