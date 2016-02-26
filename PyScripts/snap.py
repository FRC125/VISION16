import cv2
import urllib
import numpy as np
from optparse import OptionParser
from random import randint

jpg_target_path = '/jpg/image.jpg'
parser = OptionParser()
parser.add_option('-t', '--target', dest='target',
                  help='specify target camera\'s ip address, default: %default', metavar='TARGET',
                  default='10.1.25.5')
parser.add_option('-f', '--file', dest='filename',
                  help='save the image to a file', metavar='FILE',
                  default=str(randint(0, 1000000))+'.png')
parser.add_option('-w', '--window', action='store_true', dest='show_window',
                  help='show cv2 window of retrieved image')
parser.set_defaults(window=False)
(options, args) = parser.parse_args()
print 'connecting to ' + options.target
response = urllib.urlopen('http://' + options.target + jpg_target_path)
img = response.read()
cv2_img = cv2.imdecode(np.fromstring(img, dtype=np.uint8), cv2.IMREAD_COLOR)
cv2.imwrite(options.filename, cv2_img)
if options.show_window:
    cv2.imshow('image', cv2_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
