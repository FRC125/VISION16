import sys
import time
import logging
import v16Parent
import NetworkTables
from time import sleep
import random

logging.basicConfig(level=logging.DEBUG)
ip = "127.0.0.1"
DELAY_TIME = 0.1


NetworkTable.setIPAddress(ip)
NetworkTable.setClientMode()
NetworkTable.initialize()

sd = NetworkTable.getTable("visionTable")
data_table = sd.getSubTable("data")
# this table is used so that we can easily change the
# name of the networktable values we access
table_map = {'updateInProgress': 'updateInProgress', 'whichData': 'whichData',
             'canSee': 'canSee', 'offsetFromCenter': 'offsetFromCenter',
             'distance': 'distance', 'angle': 'angle'}
update_mode_map = {'ALIGNMENT': 0, 'RELATIVETARGET': 1, 'ALL': 2}


# TODO these functions should return data for the networktable based on
# their parameters, order_init_corners was given as an example
def get_can_see(order_init_corners):
    return random.choice([True, False])


def get_offset_from_center(order_init_corners):
    return random.randrange(-200, 200, 1)


def get_distance(order_init_corners):
    return random.randrange(6, 13, 1)


def get_angle(order_init_corners):
    return random.randrange(-45, 45, 1)


def updateNetworkTables():
    print('updating networktables')
    # find data that is reused for each image processing function above,
    # so we don't have to calculate the same thing multiple times
    order_init_corners = ""
    # checks which data is requested, updates corresponding data
    update_mode = sd.getInt(table_map['whichData'])
    # updates canSee and offsetFromCenter
    if (update_mode == update_mode_map['ALIGNMENT'] or
            update_mode == update_mode_map['ALL']):
        print('\tupdating alignment data')
        data_table.putBoolean(table_map['canSee'],
                              get_can_see(order_init_corners))
        data_table.putNumber(table_map['offsetFromCenter'],
                             get_offset_from_center(order_init_corners))
    # updates angle and distance
    if (update_mode == update_mode_map['RELATIVETARGET'] or
            update_mode == update_mode_map['ALL']):
        print('\tupdating relative target data')
        data_table.putNumber(table_map['angle'],
                             get_angle(order_init_corners))
        data_table.putNumber(table_map['distance'],
                             get_distance(order_init_corners))

while True:
    try:
        sleep(DELAY_TIME)
        updateInProgress = sd.getBoolean(table_map['updateInProgress'])
        if updateInProgress:
            updateNetworkTables()
            sd.putBoolean(table_map['updateInProgress'], False)
        else:
            print('networktables are up to date')
    except KeyError:
        print('Robot didn\'t initialize networktables')
