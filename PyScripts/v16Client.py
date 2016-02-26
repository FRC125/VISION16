import cv2
from v16Parent import *
from Server import *

camera_port = 0
offset_angle_moving_avg = 0

cap = cv2.VideoCapture(camera_port)

cap.set(3, 1280) #Set the width important because the default will timeout
cap.set(4, 960) #Set the height (ignore the errors printed to the console)


# Capture a single image from the camera and return it
def get_image():
 r, frame = cap.read()
 return frame

while True:

    try:
        img = get_image()

        #Thresh using the Low and High constant limits to remove noise
        initialMask = bit_color(img, LOW_THRESH, HIGH_THRESH)

        #Draw the corners onto the image
        corners = drawCorners(initialMask,img)

        #Save the image
        cv2.imwrite("test.jpg", img)

        OrderInitCorners = order_points(np.array(corners))

        LeftHeight, RightHeight = getHeightLeftRight(OrderInitCorners)
        avgHeight = (LeftHeight+RightHeight)/2
        width = getWidth(OrderInitCorners)
        aspectRatio = getAspectRatio(avgHeight, width)
        theta = getAngle(aspectRatio)
        offsetAngle = getOffsetAngle(OrderInitCorners)
        distance = getDistance(OrderInitCorners)
        offsetDistance = getOffsetDistance(theta,distance)
        
        print("Distance From Target",distance)
        print("Offset Angle", offsetAngle)
        offset_angle_moving_avg *= 0.9
        offset_angle_moving_avg += 0.1 * offsetAngle
        sendString(str(offset_angle_moving_avg))

    except ImageNotDetectedException:
        print("Can't See")
        sendString(str(5000))

                
del(cap)
