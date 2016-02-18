import time
import logging
from networktables import NetworkTable

logging.basicConfig(level=logging.DEBUG)

IP = '10.1.25.2'
NetworkTable.setIPAddress(IP)
NetworkTable.setClientMode()

sd = NetworkTable.getTable("vision")

def setDistance(distance):
    sd.putNumber("distance", distance)

def setOffsetAngle(offsetAngle):
    sd.putNumber("offsetAngle", offsetAngle)

def canSee():
    #If Target not visible, set the distance and angle to 5000
    setDistance(5000)
    setOffsetAngle(5000)
