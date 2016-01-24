import numpy as np
import cv2
import math


LOW_GREEN = [50, 100, 100]
HIGH_GREEN = [90, 255, 255]

#BGR image, HSV colors ->??????????
def bit_color(image, color_low, color_high) :
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
    contours, hierarchy = cv2.findContours(image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
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
    
    x1,y1 = corners[0]
    x2,y2 = point2

    height = abs(y1-y2)
    width = abs(x1-x2)

    return (height,width,x1,y1)

def distanceBetweenTwoPoints(point1,point2):
    x1,y1 = point1
    x2,y2 = point2

    return math.sqrt(math.pow((math.abs(x1-x2)),2) + math.pow((math.abs(y1-y2))))
def getPixelWidth(image):
    _,w,_,x1,_ = getHeightandWidth(image)
    width = len(image[0])
    return float(width) / 2 - (x1+ float(w)/2)

#Mask bit color? Do you want to remove noisy
im = resize(cv2.imread("graphics/green4.JPG"),1000,700)
mask = bit_color(im, LOW_GREEN, HIGH_GREEN)
corners = []
for point in getCorners(mask):
    point = (point[0][0], point[0][1])
    corners.append(point)
    print(point)

for corner in corners:
    cv2.circle(im,corner,20,(0,255,0))



cv2.imshow("im", im)




cv2.waitKey(0)
cv2.destroyAllWindows()

