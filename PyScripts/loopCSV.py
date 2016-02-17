import cv2
import numpy as np
import csv

distance = [9,10,11,23,23,45,1,14,17,18]
angle = [5,4,6,7,8,9,54,2,3,4]
ofile = open('data.csv', 'wb')
try:
    writer = csv.writer(ofile, delimiter='\t')
    writer.writerow("Distance")
    writer.writerow("angle")
    for i in distance:
        writer.writerow("distance[i]")
        writer.writerow("angle[i]")
finally:
    ofile.close()
