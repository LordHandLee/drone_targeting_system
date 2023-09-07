from imutils import paths
import numpy as np
import imutils
import cv2 as c1
import time

knownDistance = 72.0# Known distance from camera to face
knownWidth = 20.0# Known width of face
upper_body = c1.CascadeClassifier('front_face.xml') #load our HAAR Cascade for face detection
#upper_body = c1.CascadeClassifier('upper_body.xml')
def find_marker2(image):
    """function that detects a face and returns the
        dimension of the bounding box as a tuple of tuples"""
    gray = c1.cvtColor(image, c1.COLOR_BGR2GRAY)
    upper = upper_body.detectMultiScale(gray, 1.3, 1)
    if len(upper) >= 1:
        XY = (upper[0][0],upper[0][1])
        WH = (upper[0][2],upper[0][3])
        Z = 5
        upper1 = (XY,WH,Z) # xy, width height, Z
        return upper1

def find_marker(image): #get the PER WIDTH
    """function that detects a face and returns the
        width of the bounding box to be used to calculate the distance
        from the object(person) to the camera(drone)"""
    gray = c1.cvtColor(image, c1.COLOR_BGR2GRAY)
    upper = upper_body.detectMultiScale(gray, 1.3, 1)
    if len(upper) >= 1:
        treasure = upper[0][2]
        treasure1 = float(treasure)
        return treasure1

def distance_to_camera(knownWidth, focalLength, perWidth):
    """calculates the distance from the object to camera using triangle similarity and returns it"""
    inches1 = (knownWidth * focalLength) / perWidth
    return inches1
