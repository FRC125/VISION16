import numpy as np
import cv2
import math
from sys import argv
import getData
import csv

#LOW_GREEN = [50, 100, 100]
#HIGH_GREEN = [90, 255, 255]
LOW_GREEN = [0,0,200]
HIGH_GREEN = [100,255,255]

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
    contours, hierarchy = cv2.findContours(image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    return contours

#Binary Image (mask) ---> Four points(corners)
def getCorners(binImage):
    contours = getContours(binImage)
    x = 0
    while(x < len(contours) and not rejectShape(contours[x])):
        x = x+1
    if(not(x == len(contours))):
        convexHull = cv2.convexHull(contours[x])
        #hull = cv2.approxPolyDP(convexHull,1,True)
        for i in range(100):
            corners = cv2.approxPolyDP(convexHull, i, True)
            if len(corners) == 4:
                return corners.squeeze()
    
#Slope of two top Points -----> Angle 
def getAngle(Slope):
    a = -21.537
    b = -2.5033
    c = 10.067
    d = 22.746
    return (a*math.tan((b*Slope)+c)+d)

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
def getCenterLine(OrderedPoints):
    w = getWidth(OrderedPoints)
    center = OrderedPoints[3][0] + w/2
    return center

def distanceFromCenter(OrderedPoints):
    return 350 - getCenterLine(OrderedPoints)

#Masked Image, original Image ----> Draws corners on OriginalImage,returns the corners
def drawCorners(maskedImage,binImage):
    drawnCorners = []
    try:
        for point in getCorners(maskedImage):
            drawnCorners.append(point)
        for corner in drawnCorners:
            cv2.circle(binImage,(corner[0],corner[1]),20,(0,255,0))
        return drawnCorners
    except:
        return False
#Contour ---> returns Boolean if the contour is large enough
def rejectShape(contour):
    if(cv2.contourArea(contour) < 200):
        return False
    return True

def parse_file_name(name):
    # Here be Dragons...
    return name[len(name)-name[::-1].index("/"):name.index(".png")]

def parse_name_values(name):
    return [int(name[:name.index("f")]),int(name[name.index("t")+1:])]


if __name__ == "__main__":
    file = open('output.csv','wb')
    csvwriter = csv.writer(file, delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)
    csvwriter.writerow(['feet','angle','value'])
    reference_img = cv2.imread("7ft0.png")
    reference_img = resize(reference_img, 1000, 700)
    reference_mask = bit_color(reference_img, LOW_WHITE, HIGH_WHITE)

    img_files = getData.getFileNames(getData.DATA_FOLDER)
    comparison_img = {}
    for img_file in img_files:
        comparison_img[img_file] = bit_color(resize(cv2.imread(img_file),1000,700), LOW_WHITE, HIGH_WHITE)

    for img_file,img in comparison_img.iteritems():
        img_file_short_name = parse_file_name(img_file)
        img_comparison_value = ""
        try:
            img_comparison_value = str(compareObjectCenters(img,reference_mask))
        except:
            print(img_file_short_name + " unparsable")
            continue
        print(img_file_short_name + " : " + img_comparison_value)
        row = parse_name_values(img_file_short_name)
        row.append(img_comparison_value)
        csvwriter.writerow(row);
    cv2.waitKey(0)
    cv2.destroyAllWindows()
