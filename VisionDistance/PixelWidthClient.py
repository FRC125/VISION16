from PixelWidth import *


KNOWN_WIDTH = 20
KNOWN_DISTANCE = 24

#Store the actual Known width and height of the object as constants. 
IMAGES = ['2ft.jpg', '4ft.jpg', '6ft.jpg', 'tilt.jpg']

#Inialize Array to store the paths to the pictures (ex: IMAGES = ['pathToFirstPic.jpg','pathToSecondPic.jpg', 'soOnAnSoForth.jpg'])
#No need to specify path if pictures are in the same directory as the code 
class Runner(calculateDistance):


    def calculateFocalLength(self):
                #FOCAL LENGTH = (w x KNOWN_DISTANCE) / KNOWN_WIDTH
                return (initialIm.w*KNOWN_DISTANCE)/KNOWN_WIDTH

    def calculateDistance(self):
                #Distance = (KnownWidth x FocalLength)/pixel width
                return (KNOWN_WIDTH * FOCAL_LENGTH)/self.w


    
initialIm = Runner(IMAGES[0])
FOCAL_LENGTH = initialIm.calculateFocalLength()
finalIm = Runner(IMAGES[1])
w,h = initialIm.computeHeightWidth()


print "finalpwidth: " + str(finalIm.w)
print "initialpwidth" + str(initialIm.w)
print "focalLength " + str(FOCAL_LENGTH)

print str()


Distance = finalIm.calculateDistance()

print "Distance: " + str(Distance)
##           cv2.imshow("hello", initialIm.im)
##           cv2.waitKey(0)
##           cv2.destroyAllWindows()



   

           
 
