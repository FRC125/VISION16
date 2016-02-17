import cv2
from v16Parent import *

camera_port = 0

cap = cv2.VideoCapture(camera_port)

#If issues stem, change Height and Width Settings (Preserve Aspect Ratio)

cap.set(3, 1280) #Set the width important because the default will timeout
cap.set(4, 720) #Set the height (ignore the errors printed to the console)


# Capture a single image from the camera and return it
def get_image():
 r, frame = cap.read()
 return frame
 
img = get_image()

#Thresh using the Low and High constant limits to remove noise
initialMask = bit_color(img, LOW_GREEN, HIGH_GREEN)

#Draw the corners onto the image
corners = drawCorners(initialMask,img)

#Save the image
cv2.imwrite("test.jpg", img)

OrderInitCorners = order_points(np.array(corners))

LeftHeight, RightHeight = getHeightLeftRight
avgHeight = (LeftHeight+RightHight)/2
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
print("Offset Horizontal Distance", offserDistance)

del(cap)
