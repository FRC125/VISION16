import cv2
from v16Parent import *
from Server import *

cameraHeight = 1280
cameraWidth = 960

#Read and resize the two images (edit param to include respective path to image)
img = resize(cv2.imread("/path/to/image.jpg"),cameraHeight,cameraWidth)

#Thresh using the Low and High limits and remove noise
initialMask = bit_color(img, LOW_THRESH, HIGH_THRESH)

#Draw the corners onto the image
corners = drawCorners(initialMask,img)

#Show the image
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

cv2.imshow("im", img)
print("Distance From Target",distance)
print("Offset Angle", offsetAngle)

sendString(str(offsetAngle))

cv2.waitKey(0)
cv2.destroyAllWindows()
