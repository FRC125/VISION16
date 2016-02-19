import time
import logging
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

IP = '10.1.25.72'
socketNO = 8125



def sendString(data):
    sock.sendto(data,(IP,socketNO))
