import numpy as np
import cv2
import math


LOW_GREEN = [50, 100, 100]
HIGH_GREEN = [90, 255, 255]
#BGR image, HSV colors ->??????????

def bit_color(image, color_low, color_high):
    hsv = cv2.cvtColor (image, cv2.COLOR_BGR2HSV)
    l_green = np.array(color_low)
    u_green = np.array(color_high)
    mask = cv2.inRange (hsv, l_green, u_green)
    #ret,thresh = cv2.threshold(mask,0,255,0)
    return (mask)

def resize(im, width, height): 
    #Resize using the scale to preserve aspect ratio
    scale = min(float(width) / len(im[0]) , float(height) / len(im))
    return cv2.resize(im,(int(math.floor(len(im[0]) * scale)), int(math.floor(len(im) * scale))))

def getContours(image):
    # Depending on your version of opencv and python, findContours either returns 
    # (im, contours, hierarchy), or just (contours, hierarchy)
    # in both cases, contours is second to last.
    contours_tuple = cv2.findContours(image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = contours_tuple[-2] # get second to last item
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    return contours

#Binary Image (mask) ---> Four points(corners)
def getCorners(binImage):
    contours = getContours(binImage)
    convexHull = cv2.convexHull(contours[0])
    #hull = cv2.approxPolyDP(convexHull,1,True)
    
    for i in range(100):
        corners = cv2.approxPolyDP(convexHull, i, True)
        
        if len(corners) == 4:
            return corners
        
def getHeightandWidth(image):

    corners = getCorners(image)
    
    p1 = corners[0]
    p2 = corners[1]
    x1 = p1[0][0]
    y1 = p1[0][1]
    x2 = p2[0][0]
    y2 = p2[0][1]
    height = abs(y1-y2)
    width = abs(x1-x2)
    
    #cv2.fillConvexPoly(draw, corners, 1)
    return height,width,x1,y1

def distanceBetweenTwoPoints(point1,point2):
    x1,y1 = point1
    x2,y2 = point2

    return math.sqrt(math.pow((math.abs(x1-x2)),2) + math.pow((math.abs(y1-y2))))
    
def getPixelWidth(image):
    _,w,_,x1 = getHeightandWidth(image)
    width = len(image[0])
    return float(width) / 2 - (x1+ float(w)/2)
    
def getAngle(dist, x):
    return math.atan(float(x)/float(dist))

#NumpyArray -> NumpyArray
def order_points(pts):
    print(pts)
    
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype = "float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis = 1)
    print(s.flatten())
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

    
#Mask bit color? Do you want to remove noisy
im = cv2.imread("green4.JPG")
im = resize(im,1000,700)
mask = bit_color(im, LOW_GREEN, HIGH_GREEN)
corners = []

for point in getCorners(mask):
    point = (point[0][0], point[0][1])
    corners.append(point)
    print(point)

for corner in corners:
    cv2.circle(im,corner,20,(0,255,0))

getPixelWidth(mask)
cv2.imshow("im", im)



cv2.waitKey(0)
cv2.destroyAllWindows()

