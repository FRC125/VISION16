import sys
import time
import logging
from networktables import NetworkTable

logging.basicConfig(level=logging.DEBUG)
ip = 127.0.0.1

NetworkTable.setIPAddress(ip)
NetworkTable.setClientMode()
NetworkTable.initialize()

sd = NetworkTable.getTable("vision")
enableVision = True

while True:
    try:
        enableVision = sd.getBoolean('enableVision')
        print('enableVision: ', enableVision)
    except KeyError:
        print('enableVision: N/A')
    if enableVision:
        sd.putNumber('visionDistance', 100)  # send the distance from opencv
