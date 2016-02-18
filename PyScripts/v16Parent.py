import numpy as np
import cv2
import math

#Green
#LOW_GREEN = [50, 100, 100]
#HIGH_GREEN = [90, 255, 255]

#white
LOW_GREEN = [0,0,200]
HIGH_GREEN = [100,255,255]

#Yellow
#LOW_GREEN = [20,50,80]
#HIGH_GREEN = [80,255,255]
THETA = 70

FOV = 60.0

camera_width = 1280

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
            x = x+1
    raise ImageNotDetectedException

#Aspect Ratio ----> angle between Robot and Target
def getAngle(aspect_ratio):
    # r = 0.936
    intercept = -2.9628
    slope = 4.7953
    return math.degrees(math.atan(slope * aspect_ratio + intercept))

def getOffsetAngle(OrderedPoints):
    centerX = getCenterX(OrderedPoints)
    slope = FOV/camera_width
    intercept = -FOV/2
    return (centerX*slope)+intercept

#Ordered Corners ------> Distance
def getDistance(OrderinitCorners):
    centerHeight = getCenterY(OrderinitCorners)
    return (0.0157*centerHeight) + 4.2257

#Angle Between Robot and Target, Vertical Distance ------> Horizontal Offset Distance
def getOffsetDistance(angle, distance):
    return distance*math.cos(angle)

#Corners ------> Left and Right Heights
def getHeightLeftRight(OrderinitCorners):

    LeftHeight = abs(OrderinitCorners[0][1]-OrderinitCorners[3][1])
    RightHeight = abs(OrderinitCorners[1][1]-OrderinitCorners[2][1])

    return (LeftHeight,RightHeight)

#Height, Width ------> Aspect Ratio
def getAspectRatio(height, width):
    return height/width

def getCenterHeight(OrderinitCorners):
    rightCornerY = OrderinitCorners[2][1]
    leftCornerY = OrderinitCorners[3][1]

    return (rightCornerY+leftCornerY)/2

#Corners------->Width
def getWidth(OrderinitCorners):
    return abs(OrderinitCorners[2][0]-OrderinitCorners[3][0])

#Corners-----> slope of the top two points (y2-y1)
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

    #return the ordered coordinates (Top Left = 0, Top Right = 1, Bottom Right = 2, Bottom Left = 3)
    return rect

#Set of Ordered Points -----> x value of center line
def getCenterX(OrderedPoints):
    w = getWidth(OrderedPoints)
    center = OrderedPoints[3][0] + w/2
    return center

#Center X Position, Ordered Points ------> distance from center
def distanceFromCenterX(centerX, OrderedPoints):
    return centerX - getCenterX(OrderedPoints)

#Set of Ordered Points -----> y value of center line
def getCenterY(OrderedPoints):
    lh, rh = getHeightLeftRight(OrderedPoints)
    h = (lh + rh)/2
    center = OrderedPoints[0][1] + h/2
    return center

#Center Y-Position, Ordered Corners-------> Vertical distance from the the center.
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
    lHeight, rHeight = getHeightLeftRight(corners)
    height = (lHeight + rHeight) / 2
    wid = getWidth(corners)
    rat = max(wid / height, height / wid)
    heightRat = max(lHeight / rHeight, rHeight / lHeight)
    if(rat > 4):
        return False
    if(heightRat > 2):
        return False
    return True
