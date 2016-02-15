# getData.py

import numpy as np
import cv2
import glob, os

# Give the name of the folder where the pics are
DATA_FOLDER = "../graphics/directAtWall"

LOW_WHITE = np.array([0,0,250])
HIGH_WHITE = np.array([0,0,255])

KNOWN_DISTANCE = 0.5

# getFileNames : String -> Listof Strings
def getFileNames(DATA_FOLDER):
    cwd = os.getcwd()
    os.chdir(DATA_FOLDER)
    files = []
    for file in glob.glob("*.png"):
        files.append(DATA_FOLDER+"/"+file.lower())
    os.chdir(cwd)
    return files

# readImage : String -> Scaled Color Image
def readImage(filename):
    
    img = cv2.imread(filename)
    
    max_scaled_width = 800
    max_scaled_height = 800
    
    scale = min(max_scaled_width / len(img[0]) , max_scaled_height / len(img))
    return cv2.resize(img, (round(len(img[0]) * scale),round(len(img) * scale)))

# bit_color : BGR image, HSV colors -> Binary Image
def bit_color(image, color_low, color_high) :
    hsv = cv2.cvtColor (image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange (hsv, color_low, color_high)
    #ret,thresh = cv2.threshold(mask,0,255,0)
    return (mask)
    
# getLargestContour : Binary Image -> Numpy Array of Points
def getLargestContour(binImage):
    # Depending on your version of opencv and python, findContours either returns 
    # (im, contours, hierarchy), or just (contours, hierarchy)
    # in both cases, contours is second to last.
    contours_tuple = cv2.findContours(binImage,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = contours_tuple[-2] # get second to last item
    contours = max(contours, key=cv2.contourArea)
    return contours

# Squeezed NumpyArray -> NumpyArray
def order_points(pts):
    
    rect = np.zeros((4, 2), dtype = "float32")
    
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis = 1)
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
    
# getCorners : Binary Image (mask) -> Four points(corners) in order
#                                    (TopLeft, TopRight, BottomRight, BottomLeft)
def getCorners(binImage):
    contour = getLargestContour(binImage)
    convexHull = cv2.convexHull(contour)
    tolerance = 1
    i = 0
    while True:
        corners = cv2.approxPolyDP(convexHull, tolerance, True)
        if len(corners) > 4:
            tolerance += 1
        elif tolerance > 1 and len(corners) < 4:
            tolerance -= 1
        elif len(corners) == 4:
            return order_points(np.squeeze(corners))
        if i > 10:
            raise
            return(np.squeeze(np.array([[0,0],[0,0],[0,0],[0,0]])))
        i += 1

# getAvgHeightandWidth : BinaryImage -> (avgHeight, avgWidth)
def getAvgHeightandWidth(image):

    tl, tr, br, bl = getCorners(image)
        
    left_height = bl[1] - tl[1]
    right_height = br[1] - tr[1]
    
    bottom_width = br[0] - bl[0]
    top_width    = tr[0] - tl[0]
    
    center = ((tl[0] + tr[0] + bl[0] + br[0])/4,(tl[1] + tr[1] + bl[1] + br[1])/4)
    
    height = (left_height + right_height) / 2
    width = (top_width + bottom_width) / 2    

    return height,width,center

# makePortrait : Image -> Image
# rotates the image to the right 90 degrees
# to put it in portrait view
def makePortrait(img):
    height = len(img)
    width = len(img[0])
    if width > height:
        return cv2.transpose(img)
    else:
        return img
    
def getDataFor(filename):
    img = makePortrait(readImage(filename))
    
    mask = bit_color(img, LOW_WHITE, HIGH_WHITE)
    
    data = getAvgHeightandWidth(mask)
    
    tl, tr, br, bl = getCorners(mask)
    
    cv2.putText(img,"H="+str(data[0]), (int(data[2][0] - 1.5 * data[1]), int(data[2][1])), cv2.FONT_ITALIC, 0.5, (0,255,255))
    #cv2.line(img, (tl[0], tl[1]), (bl[0], bl[1]), (0, 255, 255), 2)
    cv2.line(img, (tl[0], tl[1]), (tl[0], int(tl[1] + data[0])), (0, 255, 255), 2)
    
    cv2.putText(img,"W="+str(data[1]), (int(data[2][0]), int(data[2][1] + data[0])), cv2.FONT_ITALIC, 0.5, (255,255,0))
    cv2.line(img, (bl[0], bl[1]), (int(bl[0] + data[1]), bl[1]), (255, 255, 0), 2)
    
    
    cv2.imshow(filename, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return(data)
    
files = getFileNames(DATA_FOLDER)
for file in files:
    try:
        height, width, center = getDataFor(file)
        spacer = " "*(50 - len(file))
        print(file + spacer + "HEIGHT:", height, "   WIDTH:", width)
    except:
        print("No Data For", file)