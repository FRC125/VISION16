import numpy as np
import cv2
import math


#Green
#LOW_GREEN = [50, 100, 100]
#HIGH_GREEN = [90, 255, 255]
#white
LOW_GREEN = [0,0,180]
HIGH_GREEN = [255,255,255]
#Yellow
# LOW_GREEN = [20,50,80]
# HIGH_GREEN = [80,255,255]

class ImageNotDetectedException:
    pass

#BGR image, HSV colors ---> masked image (no noise)
def bit_color(image, color_low, color_high) :
    hsv = cv2.cvtColor (image, cv2.COLOR_BGR2HSV)
    l_green = np.array(color_low)
    u_green = np.array(color_high)
    mask = cv2.inRange (hsv, l_green, u_green)
    return mask

#Image, width, height----->Resized Image using scale to preserve aspect ratio
def resize(im, width, height):
    scale = min(float(width) / len(im[0]) , float(height) / len(im))
    return cv2.resize(im,(int(math.floor(len(im[0]) * scale)), int(math.floor(len(im) * scale))))

#image -----> array of contours
def getContours(image):
    try:
        contours, hierarchy = cv2.findContours(image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    except:
        img, contours, hierarchy = cv2.findContours(image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    return contours

#Binary Image (mask) ---> Four points(corners)
def getCorners(binImage):
    contours = getContours(binImage)
    x = 0
    while(x < len(contours)):
        if(not goodSize(contours[x])):
            x = x+1
        else:
            convexHull = cv2.convexHull(contours[x])
            #hull = cv2.approxPolyDP(convexHull,1,True)
            for i in range(100):
                corners = cv2.approxPolyDP(convexHull, i, True)
                if len(corners) == 4:
                    corners = corners.squeeze()
                    if(goodShape(corners)):
                        return corners
                    else:
                        x = x+1
    raise ImageNotDetectedException

#Slope of two top Points -----> Angle
'''def getAngle(Slope):
    a = -21.537
    b = -2.5033
    c = 10.067
    d = 22.746
    return (a*math.tan((b*Slope)+c)+d)'''

# r = 0.887
angle_intercept = -1.0908
angle_slope = 2.3214
def getAngle(aspect_ratio):
    return math.degrees(math.atan(angle_slope * aspect_ratio + angle_intercept))

# r = 0.897
angle_with_coeff_intercept = -0.46543
angle_with_coeff_slope = 1.1143
angle_with_coeff_coeff = 1.5506
def getAngleWithCoeff(aspect_ratio):
    return angle_with_coeff_coeff *
        math.degrees(math.atan(angle_with_coeff_slope *
                  aspect_ratio + angle_with_coeff_intercept))

#Width, Angle ------> Distance
def getDistance(width,angle):
    ##VERIFY THE METHOD
    return (-0.20543*width+ 2.837*(math.sin((26.96*angle)+1.9141))+24.311)

#Corners ------> Left and Right Heights
def GetHeightLeftRight(OrderinitCorners):

    LeftHeight = abs(OrderinitCorners[0][1]-OrderinitCorners[3][1])
    RightHeight = abs(OrderinitCorners[1][1]-OrderinitCorners[2][1])

    return (LeftHeight,RightHeight)

#Corners------->Width
def getWidth(OrderinitCorners):
    return (abs(OrderinitCorners[2][0]-OrderinitCorners[3][0]))

#Corners-----> slope of top two points
def getSlope(OrderinitCorners):
    p1x = OrderinitCorners[0][0]
    p1y = OrderinitCorners[0][1]
    p2x = OrderinitCorners[1][0]
    p2y = OrderinitCorners[1][1]

    return ((p2y-p1y)/(p2x-p1x))
#NumpyArray of corners -----> NumpyArray of corners in order
def order_points(pts):
    rect = np.zeros((4, 2), dtype = "float32")

    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    pts = np.delete(pts, [np.argmin(s), np.argmax(s)], 0)

    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    #return the ordered coordinates (Top Left = 1, Top Right = 2, Bottom Right = 3, Bottom Left = 4)
    return rect

#Set of Ordered Points -----> x value of center line
def getCenterX(OrderedPoints):
    w = getWidth(OrderedPoints)
    center = OrderedPoints[3][0] + w/2
    return center

def distanceFromCenterX(centerX, OrderedPoints):
    return centerX - getCenterX(OrderedPoints)


#Set of Ordered Points -----> y value of center line
def getCenterY(OrderedPoints):
    lh, rh = GetHeightLeftRight(OrderedPoints)
    h = (lh + rh)/2
    center = OrderedPoints[0][1] + h/2
    return center


def distanceFromCenterY(centerY, OrderedPoints):
    return centerY - getCenterY(OrderedPoints)


#Masked Image, original Image ----> Draws corners on OriginalImage,returns the corners
def drawCorners(maskedImage,binImage):
    drawnCorners = []

    for point in getCorners(maskedImage):
        drawnCorners.append(point)
    for corner in drawnCorners:
        cv2.circle(binImage,(corner[0],corner[1]),20,(0,255,0))
    return drawnCorners

#Contour ---> returns Boolean if the contour is large enough
def goodSize(contour):
    if(cv2.contourArea(contour) < 200):
        return False
    return True

#corners ---> returns Boolean if the contour is right size
def goodShape(corners):
    corners = order_points(corners)
    lHeight, rHeight = GetHeightLeftRight(corners)
    height = (lHeight + rHeight) / 2
    wid = getWidth(corners)
    rat = max(wid / height, height / wid)
    heightRat = max(lHeight / rHeight, rHeight / lHeight)
    if(rat > 4):
        return False
    if(heightRat > 2):
        return False
    return True
