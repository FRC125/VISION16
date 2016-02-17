from cv2 import *
import os
import random
camera_port = 1
cap = VideoCapture(camera_port)
cap.set(3, 1280)  # Set the width important because the default will timeout
cap.set(4, 960)  # Set the height (ignore the errors printed to the console)


# Capture a single image from the camera and return it
def get_image():
    r, frame = cap.read()
    return frame


google_drive_folder = "Vision Data 2\\Pointed At Target"
userpath = os.environ['USERPROFILE']

while True:
    raw_input("Press Enter")
    name = str(random.randint(0,10000000))
    imagepath = userpath+"\\Google Drive\\"+google_drive_folder+"\\"+name+".png"
    get_image()
    imwrite(imagepath, get_image())
    print("Image saved as "+imagepath)
