import numpy as np
import cv2
import math


class calculateDistance:
                contours = []
                w = 0
                h = 0     
        
        #declare known dimensions (in meters)
        def __init__(self, im):
                self.im = cv2.imread(im)
                #self.imageThreshold(self.imageResize(self.im))
                self.KNOWN_WIDTH = 20
                self.contours = self.imageFindContours(self.im)
                self.w, self.h = self.computeHeightWidth()
                
                
        def imageResize(self, im):
                #Resize using the scale to preserve aspect ratio
                scale = min(1000 / len(self.im[0]) , 700 / len(self.im))
                self.im = cv2.resize(self.im,(int(math.floor(len(self.im[0]) * scale)), int(math.floor(len(self.im) * scale))))


        def imageThreshold(self, im):
                #ThreshHold: grab only 250-255
                cv2.threshold(self.im, 250, 255, cv2.THRESH_BINARY, self.im)


        def imageFindContours(self, im):
                #GrayScale, threshAgain, find all contours in threshed image
                imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
                ret,thresh = cv2.threshold(imgray,250,255,0)
                contours, hierarcy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

                return contours

        #Find the Largest contour (Our object), and draw a rectangle around it
        #Compute the height and width of that rectangle (in pixels)
        def computeHeightWidth(self):
                height = 0
                width = 0
                
                for contour in self.contours:
                        x,y,w,h = cv2.boundingRect(contour)
                        
                        if(h>height and w>width):
                                        height = h
                                        width = w
                                
                cv2.rectangle(self.im,(x,y),(x+w,y+h),(0,0,255),2)
                #print contours
                #print "Height: " + str(height)
                #print "Width: " + str(width)
                
                
                return(height,width)
