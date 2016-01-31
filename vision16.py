import sys
import time
import logging
from networktables import NetworkTable

logging.basicConfig(level=logging.DEBUG)
ip = 127.0.0.1

NetworkTable.setIPAddress(ip)
NetworkTable.setClientMode()
NetworkTable.initialize()
