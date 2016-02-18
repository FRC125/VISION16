import sys
import csv
from cv2 import *
from v16Parent import *
from glob import glob
from os import sep
from copy import deepcopy
def parse_filename(name):
    return name[len(name)-name[::-1].index('\\'):len(name)-name[::-1].index('.')-1]


def filename_to_data(name):
    short_name = parse_filename(name)
    return short_name.split('_')

width = 1280
height = 960

output_file = sys.argv[2]
input_folder = sys.argv[1]
paths = glob(input_folder+sep+'*.png')

file_image_map = {}

for f in paths:
    img = imread(f)
    img_copy = deepcopy(img)
    img_masked = bit_color(img, LOW_GREEN, HIGH_GREEN)
    order_init_corners = 0
    do_continue = False

    putText(img_copy,"IMAGE WILL BE IGNORED", (0,height), FONT_HERSHEY_SIMPLEX, 1,(0,255,255), 2)

    try:
        order_init_corners = order_points(np.array(drawCorners(img_masked,img)))
        putText(img,"IMAGE WILL BE SAVED", (0,height), FONT_HERSHEY_SIMPLEX, 1,(0,255,0), 2)
    except ImageNotDetectedException:
        putText(img,"IMAGE COULD NOT BE PROCESSED", (0,height), FONT_HERSHEY_SIMPLEX, 1,(0,0,255), 2)
        do_continue = True

    namedWindow('image', WINDOW_NORMAL)
    imshow('image', img)

    toggle_keep = True
    key = waitKey(0)
    while key == 88 or key == 120:
        if not do_continue:
            toggle_keep = not toggle_keep
            imshow('image', img if toggle_keep else img_copy)
        key = waitKey(0)
    if do_continue or not toggle_keep:
        continue
    l,r = GetHeightLeftRight(order_init_corners)
    avg = (l+r)/2
    aratio = avg/getWidth(order_init_corners)
    # Add any data to the dictionary here and it will be put on csv
    file_image_map[f]=[img,{'aspect_ratio': aratio,
     'estimate_angle': getAngle(aratio)}]
'''{'width': getWidth(order_init_corners),
                            'height_left': l,
                            'height_right': r,
                            'height_avg': avg,
                            'rel_vertical': distanceFromCenterY(height/2,order_init_corners),
                            'rel_horizontal': distanceFromCenterX(width/2,order_init_corners)}'''

img_count = len(file_image_map)
print(str(img_count) + ' image'+ (' was' if img_count == 1 else 's were') +' able to be processed')
if img_count == 0:
    print("aborting...")
    sys.exit(0)

f = open(output_file, 'wb')
writer = csv.writer(f, delimiter = ',', quotechar = '\"', quoting = csv.QUOTE_ALL)
writer.writerow(['distance','angle']+list(list(file_image_map.viewvalues())[0][1].viewkeys()))
for k, v in file_image_map.iteritems():
    writer.writerow(filename_to_data(k)+list(v[1].viewvalues()))
