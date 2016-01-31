import numpy as np
import cv2
import math


LOW_GREEN = [50, 100, 100]
HIGH_GREEN = [90, 255, 255]
KNOWN_DISTANCE = 0.5

# BGR image, HSV colors ->??????????
def bit_color(image, color_low, color_high) :
    hsv = cv2.cvtColor (image, cv2.COLOR_BGR2HSV)
    l_green = np.array(color_low)
    u_green = np.array(color_high)
    mask = cv2.inRange (hsv, l_green, u_green)

    # ret,thresh = cv2.threshold(mask,0,255,0)
    return (mask)

def resize(im, width, height) :
    # Resize using the scale to preserve aspect ratio
    scale = min(float(width) / len(im[0]) , float(height) / len(im))
    return cv2.resize(im,(int(math.floor(len(im[0]) * scale)), int(math.floor(len(im) * scale))))

def getContours(image) :
    contours, hierarchy = cv2.findContours(image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    return contours

# Binary Image (mask) ---> Four points(corners)
def getCorners(binImage) :
    contours = getContours(binImage)
    convexHull = cv2.convexHull(contours[0])

    # hull = cv2.approxPolyDP(convexHull,1,True)
    for i in range(100) :
        corners = cv2.approxPolyDP(convexHull, i, True)

        if len(corners) == 4 :
                return corners

def averageDxDy(binImage1,binImage2) :
    # calculate distance between the corners, then return the average
    # ^This gives the maginutude and direction (-/+) of your translation

    image1Corners = np.array(getCorners(binImage1))
    image2Corners = np.array(getCorners(binImage2))

    dXdY = image2Corners-image1Corners
    Cols = dXdY.shape
    dX = 0.0
    print(dXdY)
    for i in range(dXdY.shape[0]) :
        dX += dXdY[i][0][0]

    dXavg = dX/4

    dY = 0.0
    for i in range(dXdY.shape[1]) :
        dY += dXdY[i][0][1]
        dYavg = dY/4

    return (dXavg,dYavg)

def getHeightandWidth(image) :
     # cv2.fillConvexPoly(draw, corners, 1)
    corners = getCorners(image)
    p1 = corners[0]
    p2 = corners[1]
    x1 = p1[0][0]
    y1 = p1[0][1]
    x2 = p2[0][0]
    y2 = p2[0][1]
    height = abs(y1-y2)
    width = abs(x1-x2)

    return height,width,x1,y1

# four points(corners) -> float
def getArea(corners) :
    orders = order_points(np.array(corners))

    tl = orders[0]
    tr = orders[1]
    br = orders[2]
    bl = orders[3]

    x1 = (tl[0] + bl[0]) / 2
    x2 = (tr[0] + br[0]) / 2
    y1 = (tl[1] + tr[1]) / 2
    y2 = (bl[1] + br[1]) / 2
    dx = x1 - x2
    dy = y1 - y2

    return (dx * dy)

# four points(current, reference) -> proportion(float)
def areaProportion(current,reference) :
    return getArea(current)/getArea(reference)

def calcDist(current, reference, knowDist) :
    return areaProportion(current, reference) * knowDist

def distanceBetweenTwoPoints(point1,point2) :
    x1,y1 = point1
    x2,y2 = point2
    return math.sqrt(math.pow((math.abs(x1-x2)),2) + math.pow((math.abs(y1-y2))))

def getPixelWidth(image) :
    _,w,_,x1 = getHeightandWidth(image)
    width = len(image[0])
    return float(width) / 2 - (x1+ float(w)/2)

def getAngle(dist, x) :
    return math.atan(float(x)/float(dist))

# NumpyArray -> NumpyArray
def order_points(pts) :
    # print(pts)
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype = "float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis = 1)
    #print(s.flatten())
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    pts = np.delete(pts, [np.argmin(s), np.argmax(s)], 0)

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    # return the ordered coordinates
    return rect

def calculateDistance(initialMask,finalMask) :
    _,initialPixelWidth,_,_  =  getHeightandWidth(initialMask)
    _,finalPixelWidth,_,_  =  getHeightandWidth(finalMask)
    ratio = (float(initialPixelWidth)/float(finalPixelWidth))
    return KNOWN_DISTANCE/(1-ratio)

# Read and resize the two images
initialIm = resize(cv2.imread("green4.JPG"),1000,700)
finalIm = resize(cv2.imread("dist3.JPG"),1000,700)

# Thresh and remove noise
initialMask = bit_color(initialIm, LOW_GREEN, HIGH_GREEN)
finalMask = bit_color(finalIm, LOW_GREEN, HIGH_GREEN)

initialCorners = []
finalCorners = []

for point in getCorners(initialMask) :
    point = (point[0][0], point[0][1])
    initialCorners.append(point)
    # print(point)

for corner in initialCorners :
    cv2.circle(initialIm,corner,20,(0,255,0))

for point in getCorners(finalMask) :
    point = (point[0][0], point[0][1])
    finalCorners.append(point)
    # print(point)

for corner in finalCorners :
    cv2.circle(finalIm,corner,20,(0,255,0))

# getPixelWidth(mask)
# print(getArea(corners))
cv2.imshow("im", initialIm)
cv2.imshow("im2", finalIm)

Distance = calculateDistance(initialMask, finalMask)
print Distance

cv2.waitKey(0)
cv2.destroyAllWindows()
