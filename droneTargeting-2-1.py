"""simple UAV Drone targeting system using computer vision"""
import cv2 as c1
import time
from droneFunctions import find_marker, find_marker2, distance_to_camera
"""MAKE IT SO IT TRACKS USING KCF AND CSRT. USE CSRT TO POSITION DRONE AND KCF TO KEEP TRACK. IF KCF FAILS, SEARCH AGAIN FOR FACE"""
knownDistance = 72.0# Known distance from camera to face
knownWidth = 20.0# Known width of face
cap = c1.VideoCapture(0) #capture the video input
##width  = cap.get(c1.CAP_PROP_FRAME_WIDTH)   # float
##height = cap.get(c1.CAP_PROP_FRAME_HEIGHT)
box = None
tracker = c1.TrackerKCF_create()
tracker2 = c1.TrackerKCF_create()#create csrt tracker to track image located on screen
marker = None
focalLength = (55 * knownDistance) / knownWidth #Formula to find the focal length
time.sleep(2)

def recur(boxer,frame):
    if boxer is None: #since boxer is nothing, lets detect some humans and get the width
            marker = find_marker(frame) #returns the width of the bounding box
            if bool(marker) == True: #if a human face is detected lets process the bounding box
                marker3 = find_marker2(frame) #returns the position and dimensions of the bounding box as a tuple of tuples
                X = marker3[0][0]
                Y = marker3[0][1]
                W = marker3[1][0]
                H = marker3[1][1]
                boxer = (X,Y,W,H) #package the position and dimensions into a single tuple so we can pass to the tracker
                inches = distance_to_camera(knownWidth, focalLength, marker) #gets the distance from the object to the camera by using triangle similarity
    else: #since we have initialized "boxer" with bounding box data we can now also initialize our csrt tracker
        #also stops detecting faces/humans since boxer is not None
        tracker.init(frame, boxer) #initialize tracker
        (success, box) = tracker.update(frame) #Updates the tracker and returns "True" or "False" for success and BBox dimensions, then stores each into their own seperate variable
        if success: #if successful
            print("SUCESS")
            (x, y, w, h) = [int(v) for v in box] #stores the updated position and dimensions from the tracker
            inches = distance_to_camera(knownWidth, focalLength, w)#calculates the distance based on the width from the tracker BBox and not the Haar Cascade BBox
            feet = inches/12
            c1.rectangle(frame, (x, y), (x + w, y + h),(255, 255, 0), 2) #draw box to the screen
            """Here is where we send flight instructions to drone based on position of the bounding box using functions from
                the drone flight controller API""" #need to find the right range of coordinates
            #else success == False, continue so we can reacquire target
            c1.rectangle(frame, (250, 150), (400, 300),(0, 255, 0), 2)
            c1.putText(frame, "%.2fft" % (inches / 12),(frame.shape[1] - 200, frame.shape[0] - 20), c1.FONT_HERSHEY_SIMPLEX,2.0, (0, 255, 0), 3) #display the distance
##            if x < 250:
##                print("TURNING LEFT")
##            elif x + w > 400:
##                print("TURNING RIGHT")
##            elif y < 150:
##                print("INCREASING ALTITUDE")
##            elif y + h > 300:
##                print("DECRESING ALTITUDE")
##            elif feet >= 5:
##                print("MOVING FORWARD")
##            elif feet <= 3:
##                print("MOVING REVERSE")
##            else:
##                print("ON TARGET")
        else:
            tracker.clear()
            recur(boxer,frame)
            
def track():
    boxer = None
    tracker = c1.TrackerKCF_create()
    tracker1 = c1.TrackerCSRT_create()
    while True:
        res, frame = cap.read()
        if boxer is None: #since boxer is nothing, lets detect some humans and get the width
            marker = find_marker(frame) #returns the width of the bounding box
            if bool(marker) == True: #if a human face is detected lets process the bounding box
                marker3 = find_marker2(frame) #returns the position and dimensions of the bounding box as a tuple of tuples
                X = marker3[0][0]
                Y = marker3[0][1]
                W = marker3[1][0]
                H = marker3[1][1]
                boxer = (X,Y,W,H) #package the position and dimensions into a single tuple so we can pass to the tracker
                inches = distance_to_camera(knownWidth, focalLength, marker) #gets the distance from the object to the camera by using triangle similarity
        else: #since we have initialized "boxer" with bounding box data we can now also initialize our csrt tracker
            #also stops detecting faces/humans since boxer is not None
            """create new CSRT tracker to run alongside the KCF tracker to calculate distance. If KCF fails, destroy CSRT and resume tracking humans"""
            tracker.init(frame, boxer) #initialize tracker
            (success, box) = tracker.update(frame) #Updates the tracker and returns "True" or "False" for success and BBox dimensions, then stores each into their own seperate variable
            tracker1.init(frame,boxer)
            (success1,box1) = tracker1.update(frame)
            if success: #if successful
                (x, y, w, h) = [int(v) for v in box] #stores the updated position and dimensions from the tracker
                (xr, yr, wr, hr) = [int(k) for k in box1]
                inches = distance_to_camera(knownWidth, focalLength, wr)#calculates the distance based on the width from the tracker BBox and not the Haar Cascade BBox
                feet = inches/12
                c1.rectangle(frame, (x, y), (x + w, y + h),(255, 255, 0), 2) #draw box to the screen
                """Here is where we send flight instructions to drone based on position of the bounding box using functions from
                    the drone flight controller API""" #need to find the right range of coordinates
                #else success == False, continue so we can reacquire target
                c1.rectangle(frame, (250, 150), (400, 300),(0, 255, 0), 2)
                c1.putText(frame, "%.2fft" % (inches / 12),(frame.shape[1] - 200, frame.shape[0] - 20), c1.FONT_HERSHEY_SIMPLEX,2.0, (0, 255, 0), 3) #display the distance
    ##            if x < 250:
    ##                print("TURNING LEFT")
    ##            elif x + w > 400:
    ##                print("TURNING RIGHT")
    ##            elif y < 150:
    ##                print("INCREASING ALTITUDE")
    ##            elif y + h > 300:
    ##                print("DECRESING ALTITUDE")
    ##            elif feet >= 5:
    ##                print("MOVING FORWARD")
    ##            elif feet <= 3:
    ##                print("MOVING REVERSE")
    ##            else:
    ##                print("ON TARGET")
            else:
                boxer = None
                if boxer is None: #since boxer is nothing, lets detect some humans and get the width
                    marker = find_marker(frame) #returns the width of the bounding box
                    if bool(marker) == True: #if a human face is detected lets process the bounding box
                        marker3 = find_marker2(frame) #returns the position and dimensions of the bounding box as a tuple of tuples
                        X = marker3[0][0]
                        Y = marker3[0][1]
                        W = marker3[1][0]
                        H = marker3[1][1]
                        boxer = (X,Y,W,H)#package the position and dimensions into a single tuple so we can pass to the tracker
                        inches = distance_to_camera(knownWidth, focalLength, marker) #gets the distance from the object to the camera by using triangle similarity
                #else: #since we have initialized "boxer" with bounding box data we can now also initialize our csrt tracker
                    #also stops detecting faces/humans since boxer is not None
                        tracker = c1.TrackerKCF_create()
                        tracker.init(frame, boxer) #initialize tracker
                        (success, box) = tracker.update(frame) #Updates the tracker and returns "True" or "False" for success and BBox dimensions, then stores each into their own seperate variable
                        tracker1 = c1.TrackerCSRT_create()
                        tracker1.init(frame,boxer)
                        (success1, box1) = tracker1.update(frame)
                        """create new CSRT tracker to run alongside the KCF tracker to calculate distance. If KCF fails, destroy CSRT and resume tracking humans"""
                        if success: #if successful
                            (x, y, w, h) = [int(v) for v in box] #stores the updated position and dimensions from the tracker
                            (xr, yr, wr, hr) = [int(k) for k in box1]
                            inches = distance_to_camera(knownWidth, focalLength, wr)#calculates the distance based on the width from the tracker BBox and not the Haar Cascade BBox
                            feet = inches/12
                            c1.rectangle(frame, (x, y), (x + w, y + h),(255, 255, 0), 2) #draw box to the screen
                            """Here is where we send flight instructions to drone based on position of the bounding box using functions from
                                the drone flight controller API""" #need to find the right range of coordinates
                            #else success == False, continue so we can reacquire target
                            c1.rectangle(frame, (250, 150), (400, 300),(0, 255, 0), 2)
                            c1.putText(frame, "%.2fft" % (inches / 12),(frame.shape[1] - 200, frame.shape[0] - 20), c1.FONT_HERSHEY_SIMPLEX,2.0, (0, 255, 0), 3)
        c1.imshow('frame',frame) #displays the frame to the screen

        if c1.waitKey(1) & 0xFF == ord('q'): #stops the program if q is pressed
            break
track()
