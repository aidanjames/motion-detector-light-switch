from switch_manager import SwitchManager
import time
from imutils.video import VideoStream
import datetime
import imutils
import cv2
from sunset import past_sunset


light_on = False

while not light_on:

    # Only start recording if it's already past sunset (note this is LONDON sunset)
    if past_sunset():

        # Initialise light manager
        switches = SwitchManager()
        device = switches.find_devices()[0].get_alias()

        # Start capturing video from the webcam and give enough time to get out of the room so that the base
        # picture is of an empty room.
        vs = VideoStream(src=0).start()
        time.sleep(10.0)

        # initialize the first frame in the video stream
        firstFrame = None

        # loop over the frames of the video
        while not light_on:
            # grab the current frame
            frame = vs.read()

            # if the frame could not be grabbed, something's not right.
            if frame is None:
                break

            # resize the frame, convert it to grayscale, and blur it
            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # if the first frame is None, initialize it
            if firstFrame is None:
                print(f"{datetime.datetime.now()}: Storing reference frame.")
                firstFrame = gray
                continue

            # compute the absolute difference between the current frame and first frame
            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

            # dilate the thresholded image to fill in holes, then find contours on thresholded image
            thresh = cv2.dilate(thresh, None, iterations=2)
            contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)

            # loop over the contours
            for contour in contours:
                # if the contour is too small, ignore it (can tweak this value)
                if cv2.contourArea(contour) < 100:
                    continue

                if not light_on:
                    print(f"{datetime.datetime.now()}: Motion detected")
                    switches.switch_on(device)
                    light_on = True

    else:
        # If it's before sunset we only need to check every minute
        time.sleep(60)
