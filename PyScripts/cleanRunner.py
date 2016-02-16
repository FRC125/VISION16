import cv2
from v16Parent import *

#Read and resize the two images

im = resize(cv2.imread("/Users/MichaelLaposata/Desktop/directAtWall/photo 3.jpg"),1000,700)


#Thresh using the Low and High limits and remove noise
initialMask = bit_color(img, LOW_GREEN, HIGH_GREEN)

#Draw the corners onto the image
corners = drawCorners(initialMask,img)
#Show the image
cv2.imshow("im", img)
OrderInitCorners = order_points(np.array(corners))
lr = LOW_THRESHOLDLeftRight(OrderInitCorners)
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
