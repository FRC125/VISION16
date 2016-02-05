import cv2
from cleanCode import *

#Read and resize the two images
im = resize(cv2.imread("NAMEOFPICTURE.png"),1000,700)

#Thresh using the Low and High limits and remove noise
initialMask = bit_color(im, LOW_GREEN, HIGH_GREEN)

#Draw the corners onto the image
drawCorners(initialMask,im)

#Show the image
cv2.imshow("im", im)


OrderInitCorners = order_points(np.array(drawCorners(initialMask,im)))

slope = getSlope(OrderInitCorners)
width = getWidth(OrderInitCorners)
theta = getAngle(slope)
distance = getDistance(width,30)

print("distance",distance)
print("theta",theta)

#print OrderInitCorners



cv2.waitKey(0)
cv2.destroyAllWindows()
