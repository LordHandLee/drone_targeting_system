Detects a face using a HAAR cascade classifier. Once a face is detected, it then proceeds to track the face across the screen using the KCF and CSRT tracking algorithms. Finally, it simultaneously calculates the distance from the face to the camera using the camera focal length and triangle similarity. 

This code was used as part of a rudimentary drone targeting system in which the drone detects a person's face and then follows the person, maintaining a certain distance between the target and the drone.

Written using Python and OpenCV.

## The drone ##

![Image](/the_drone.png)
