import cv2
from v16Parent import *
import math
#Read and resize the two images

im = resize(cv2.imread("/Users/MichaelLaposata/Desktop/directAtWall/6ft30.png"),1000,700)


#Thresh using the Low and High limits and remove noise
initialMask = bit_color(im, LOW_GREEN, HIGH_GREEN)

#Draw the corners onto the image
corners = drawCorners(initialMask,im)
#Show the image
cv2.imshow("im", im)
OrderInitCorners = order_points(np.array(corners))
GetHeightLeftRight(OrderInitCorners)
#allows the code to not throw an error if the image does not contain a target
#try:
    
slope = getSlope(OrderInitCorners)
width = getWidth(OrderInitCorners)
theta = getAngle(slope)
angle = findAngle(OrderInitCorners)*180/math.pi
distance = getDistance(width,30)
print("angle",angle)
print("distance",distance)
print("theta",theta)
#except:
#    print("fail")
    
cv2.waitKey(0)
cv2.destroyAllWindows()
