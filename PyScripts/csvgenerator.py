import sys
import csv
from cv2 import *
from v16Parent import *
from glob import glob
from os import sep

def parse_filename(name):
    return name[len(name)-name[::-1].index('\\'):len(name)-name[::-1].index('.')-1]


def filename_to_data(name):
    short_name = parse_filename(name)
    return short_name.split('_')

output_file = sys.argv[2]
input_folder = sys.argv[1
]
paths = glob(input_folder+sep+'*.png')

file_image_map = {}

for f in paths:
    img = imread(f)
    img_masked = bit_color(img, LOW_GREEN, HIGH_GREEN)
    order_init_corners = 0
    try:
        order_init_corners = order_points(np.array(drawCorners(img_masked,img)))
    except ImageNotDetectedException:
        continue
    # Add any data to the dictionary here and it will be put on csv
    file_image_map[f]=[img,{'width': getWidth(order_init_corners),
                            'height_LR': GetHeightLeftRight(order_init_corners),
                            'rel_vertical': distanceFromCenterY(960/2,order_init_corners),
                            'rel_horizontal': distanceFromCenterX(1280/2,order_init_corners)}]

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
