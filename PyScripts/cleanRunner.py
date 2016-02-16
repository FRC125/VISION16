import cv2
from v16Parent import *

#Read and resize the two images

img = cv2.imread("IMG_0856.png",0)


#Thresh using the Low and High limits and remove noise
initialMask = bit_color(img, LOW_GREEN, HIGH_GREEN)

#Draw the corners onto the image
corners = drawCorners(initialMask,img)
#Show the image
cv2.imshow("im", img)
OrderInitCorners = order_points(np.array(corners))
lr = LOW_THRESHOLDLeftRight(OrderInitCorners)
#allows the code to not throw an error if the image does not contain a target
try:

    slope = getSlope(OrderInitCorners)
    width = getWidth(OrderInitCorners)
    theta = getAngle(slope)
    distance = getDistance(width,30)
    print("height LR",lr)
    print("width",width)
except:
    print("fail")

cv2.waitKey(0)
cv2.destroyAllWindows()
