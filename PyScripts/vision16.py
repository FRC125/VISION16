import sys
import time
import logging
from networktables import NetworkTable
from time import sleep
from v16Parent import *
import random

# NetworkTable configuration
logging.basicConfig(level=logging.DEBUG)
ip = "127.0.0.1"
NetworkTable.setIPAddress(ip)
NetworkTable.setClientMode()
NetworkTable.initialize()
sd = NetworkTable.getTable("visionTable")
data_table = sd.getSubTable("data")

DELAY_TIME = 0.1

# this table is used so that we can easily change the
# name of the networktable values we access
table_map = {'updateInProgress': 'updateInProgress', 'whichData': 'whichData',
             'canSee': 'canSee', 'offsetFromCenter': 'offsetFromCenter',
             'distance': 'distance', 'angle': 'angle'}
update_mode_map = {'ALIGNMENT': 0, 'RELATIVETARGET': 1, 'ALL': 2}

# camera configuration
camera_port = 0
cap = cv2.VideoCapture(camera_port)
cap.set(3, 960)  # Set the width important because the default will timeout
cap.set(4, 544)  # Set the height (ignore the errors printed to the console)


# Capture a single image from the camera and return it
def get_image():
    r, frame = cap.read()
    return frame


# TODO these functions should return data for the networktable based on
# their parameters, order_init_corners was given as an example
def get_offset_from_center(order_init_corners):
    return distanceFromCenter(order_init_corners)


def get_distance(width, angle):
    return getDistance(width, angle)


def get_angle(slope):
    return getAngle(slope)


def update_network_tables():
    print('updating networktables')
    # find data that is reused for each image processing function above,
    # so we don't have to calculate the same thing multiple times
    input_image = get_image()
    input_image_masked = bit_color(input_image, LOW_GREEN, HIGH_GREEN)
    order_init_corners = ""
    try:
        order_init_corners = order_points(np.array(drawCorners
                                          (input_image_masked, input_image)))
    except(ImageNotDetectedException):
        print('\timage not detected')
        data_table.putBoolean(table_map['canSee'], False)
        return
    # checks which data is requested, updates corresponding data
    update_mode = sd.getInt(table_map['whichData'])
    # updates canSee and offsetFromCenter
    if (update_mode == update_mode_map['ALIGNMENT'] or
            update_mode == update_mode_map['ALL']):
        print('\tupdating alignment data')
        data_table.putBoolean(table_map['canSee'], True)
        data_table.putNumber(table_map['offsetFromCenter'],
                             get_offset_from_center(order_init_corners))
    # updates angle and distance
    if (update_mode == update_mode_map['RELATIVETARGET'] or
            update_mode == update_mode_map['ALL']):
        slope = getSlope(order_init_corners)
        width = getWidth(order_init_corners)
        angle = get_angle(slope)
        print('\tupdating relative target data')
        data_table.putNumber(table_map['angle'], angle)
        data_table.putNumber(table_map['distance'],
                             get_distance(width, angle))

# main loop
while True:
    try:
        sleep(DELAY_TIME)
        # checks if it should update data
        update_in_progress = sd.getBoolean(table_map['updateInProgress'])
        if update_in_progress:
            update_network_tables()
            # informs DataController that update is done
            sd.putBoolean(table_map['updateInProgress'], False)
        else:
            print('networktables are up to date')
    except KeyError:
        print('Robot didn\'t initialize networktables')
