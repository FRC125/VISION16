# VISION16 [![Build Status](https://travis-ci.org/FRC125/VISION16.svg?branch=master)](https://travis-ci.org/FRC125/VISION16)

Nutrons Vision 2016 Library (Python)

Sources: OpenCV

![diagram](http://imgur.com/D0tNQ3l "Diagram of how VISION16 works")

##Distance From Target:

	Method: getDistance()

	Parameters: OrderInitCorners

		•Corners of processed image in order, starting with top right and goes clockwise

##Angle Between Robot and Target:

	Method: getAngle()

	Parameters: aspectRatio

		•The ratio between the height and width of processed image

##Offset Angle:

	Method: getOffsetAngle()

	Parameters: OrderInitCorners

		•Corners of processed image in order, starting with top left and goes clockwise

##Offset Horizontal Distance:

	Method: getOffsetDistance()

	Parameters: theta, distance

		•theta is Angle Between Robot and Target

		•distance is Distance From Target
