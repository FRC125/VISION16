import cv2
from v16Parent import *

camera_port = 0

cap = cv2.VideoCapture(camera_port)
cap.set(3, 960) #Set the width important because the default will timeout
cap.set(4, 544) #Set the height (ignore the errors printed to the console)


# Capture a single image from the camera and return it
def get_image():
 r, frame = cap.read()
 return frame
 
im = get_image()


#Thresh using the Low and High constant limits to remove noise
initialMask = bit_color(im, LOW_GREEN, HIGH_GREEN)

#Draw the corners onto the image
drawCorners(initialMask,im)

#Save the image
cv2.imwrite("test.jpg", im)


OrderInitCorners = order_points(np.array(drawCorners(initialMask,im)))

slope = getSlope(OrderInitCorners)
width = getWidth(OrderInitCorners) * (103.0/186)
theta = getAngle(slope)
distance = getDistance(width,0)

print("distance",distance)
print("theta",theta)
print("Width", width)

#print OrderInitCorners

del(cap)
