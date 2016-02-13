import cv2
import v16Parent

#Read and resize the two images
im = resize(cv2.imread("noTarget.png"),1000,700)

#Thresh using the Low and High limits and remove noise
initialMask = bit_color(im, LOW_GREEN, HIGH_GREEN)

#Draw the corners onto the image
corners = drawCorners(initialMask,im)
#Show the image
cv2.imshow("im", im)

try:
    OrderInitCorners = order_points(np.array(corners))
    GetHeightLeftRight(OrderInitCorners)
    slope = getSlope(OrderInitCorners)
    width = getWidth(OrderInitCorners)
    theta = getAngle(slope)
    distance = getDistance(width,30)
    print("distance",distance)
    print("theta",theta)
except:
    print("fail")
    
cv2.waitKey(0)
cv2.destroyAllWindows()
