#!/usr/bin/python3
from __future__ import print_function
PROG_VERSION = "0.98"

import logging
# Setup Logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")
logging.info("Loading Python Libraries ...")
import os
import sys
import time
import datetime
import math
import cv2
import subprocess
import logging

CONFIG_FILENAME = "config.py"
if os.path.exists(CONFIG_FILENAME):
    # Read Configuration variables from config.py file
    try:
        logging.info("Import Settings from %s", CONFIG_FILENAME)
        from config import *
    except ImportError:
        logging.error("Problem Importing configuration variables from %s" %
                      CONFIG_FILENAME)
        sys.exit(1)
else:
    logging.error("Configuration File Not Found %s" % CONFIG_FILENAME)
    sys.exit(1)

PROG_NAME = os.path.basename(__file__)

# ------------------------------------------------------------------------------
def show_settings(filename):
    '''
    Display program configuration variable settings
    read config file and print each decoded line
    '''
    with open(filename, 'rb') as f:
        for line in f:
            print(line.decode().strip())
    print("")


# ------------------------------------------------------------------------------
def check_picam():
    '''
    Test for legacy picamera setup then libcamera picamera2 setup and
    return results or None.
    '''
    # Check for legacy pi camera module installed and enabled
    logging.info("Check for Legacy Pi Camera Module with command - vcgencmd get_camera")
    camResult = subprocess.check_output("vcgencmd get_camera", shell=True)
    camResult = camResult.decode("utf-8")
    camResult = camResult.replace("\n", "")
    params = camResult.split()
    for x in range(0,2):
        if params[x].find("0") >= 0:
            logging.warning("Detected Problem with Pi Camera Module per %s", params[x])
            logging.info("Check Cables and/or Legacy Camera using sudo raspi-config")
        else:
            logging.info("Success: Legacy Pi Camera is %s", camResult)
            return "pilegacy"

    # Check for Libcamera pi camera module installed and enabled
    logging.info("Check if picamera2 libcamera Exists ...")
    if os.path.exists("/usr/bin/libcamera-still"):
        if os.path.exists("im_test.jpg"):
            os.remove("im_test.jpg")
        p = subprocess.run([ '/usr/bin/libcamera-still', '-v', '0', '-n', 'off', '-o', 'im_test.jpg' ])
        err = p.returncode
        if err != 0:
            logging.error("Problem testing Pi Lib Camera Errorcode = ", err)
            return None
        logging.info("Check Lib Camera output with test image")
        if os.path.exists("im_test.jpg"):
            os.remove("im_test.jpg")
            logging.info("Success: Found Pi libcamera")
            return "pilibcam"
        else:
            logging.error("Problem with Pi Lib Camera Configuration")
            return None
    else:
        logging.error("picamera2 libcamera Install Not Found.")
        logging.info("Verify libcamera is installed and working")
        return None


# ------------------------------------------------------------------------------
def get_image_name(path, prefix):
    '''
    build image file names by number sequence or
    date/time Added tenth of second
    '''
    rightNow = datetime.datetime.now()
    filename = "%s/%s%04d%02d%02d-%02d%02d%02d%d.jpg" % (
        path,
        prefix,
        rightNow.year,
        rightNow.month,
        rightNow.day,
        rightNow.hour,
        rightNow.minute,
        rightNow.second,
        rightNow.microsecond / 100000,
    )
    return filename


# ------------------------------------------------------------------------------
def timer_end(timer_start, timer_sec):
    '''
    Check if timelapse timer has expired
    Return updated start time status of expired timer True or False
    '''
    rightNow = datetime.datetime.now()
    timeDiff = (rightNow - timer_start).total_seconds()
    if timeDiff >= timer_sec:
        return True
    else:
        return False


# ------------------------------------------------------------------------------
def get_motion_track_point(grayimage1, grayimage2):
    '''
    Process two grayscale images.
    check for motion and return center point
    of motion for largest contour.
    '''
    movement_center = ()
    # Get differences between the two greyed images
    differenceimage = cv2.absdiff(grayimage1, grayimage2)
    # Blur difference image to enhance motion vectors
    differenceimage = cv2.blur(differenceimage, (BLUR_SIZE, BLUR_SIZE))
    # Get threshold of blurred difference image
    # based on THRESHOLD_SENSITIVITY variable
    retval, thresholdimage = cv2.threshold(
        differenceimage, THRESHOLD_SENSITIVITY, 255, cv2.THRESH_BINARY
    )
    try:
        # opencv2 syntax default
        contours, hierarchy = cv2.findContours(
            thresholdimage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
    except ValueError:
        # opencv 3 syntax
        thresholdimage, contours, hierarchy = cv2.findContours(
            thresholdimage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
    if contours:
        c = max(contours, key = cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(c)
        if w * h <= TRACK_MIN_AREA:
            return None
        movement_center = (int(x + w / 2), int(y + h / 2))
    return movement_center


# ------------------------------------------------------------------------------
def track_motion_distance(xy1, xy2):
    '''
    Return the triangulated distance between two tracking locations
    '''
    x1, y1 = xy1
    x2, y2 = xy2
    trackLen = int(abs(math.hypot(x2 - x1, y2 - y1)))
    return trackLen


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    if SHOW_SETTINGS:
        show_settings(config_filename)

    if not os.path.exists(IM_DIR):  # Check if image directory exists
        os.makedirs(IM_DIR)  # Create directory if Not Found

    logging.info("%s ver %s written by Claude Pageau", PROG_NAME, PROG_VERSION)
    if WEBCAM_ON or IPCAM_ON:
        if IPCAM_ON:
            cam_src = IPCAM_SRC
            cam = "IPCamera " + cam_src
        else:
            cam_src = WEBCAM_SRC
            cam = "WEBCamera " + str(cam_src)

        logging.info("Start Stream Thread: %s", cam)
        if not os.path.exists('streamwebcam.py'):
            logging.error("Import Problem. streamwebcam.py File Not Found.")
            sys.exit(1)
        try:
            from streamwebcam import WebcamStream
        except ImportError:
            logging.error("Import Failed for streamwebcam.py")
            sys.exit(1)
        vs = WebcamStream(src=cam_src, size=IM_SIZE).start()
        time.sleep(3) # Wait for stream to settle down

    else:
        cam = check_picam()   # Detect if picamera or picamera2 configured
        if cam is not None:
            logging.info("Start Stream Thread: %s", cam)
            if cam == "pilibcam":
                if not os.path.exists('streampilibcam.py'):
                    logging.error("streampilibcam.py File Not Found.")
                    sys.exit(1)
                try:
                    from streampilibcam import PiLibCamStream
                except ImportError:
                    logging.error("Failed Import of streampilibcam.py")
                    sys.exit(1)                    
                vs = PiLibCamStream(size=IM_SIZE,
                                    im_vflip=IM_VFLIP,
                                    im_hflip=IM_HFLIP).start()

            elif cam == "pilegacy":
                if not os.path.exists('streampilegacycam.py'):
                    logging.error("pilegacycamsteam.py File Not Found.")
                    sys.exit(1)
                try:  # Add this check in case running on non RPI platform using web cam
                    from streampilegacycam import PiLegacyCamStream
                except ImportError:
                    logging.error("Could Not Import streampilegacycam.py")
                    sys.exit(1)
                vs = PiLegacyCamStream(size=IM_SIZE,
                                       hflip=IM_HFLIP,
                                       vflip=IM_VFLIP).start()
            logging.info("Wait ...")
            time.sleep(5)  # Allow Camera to warm up
        else:
            logging.warning("Could not Find a PI Camera and/or Configuration")
            logging.warning("Investigate Problem.")
            sys.exit(1)

    # initialize first gray image
    start_track = True
    track_hist = []
    image1 = vs.read()
    grayimage1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    im_height, im_width, _ = image1.shape
    if TRACK_TRIG_AUTO:
        # Auto calculate variables below
        TRACK_TRIG_LEN = int(im_width / 8)  # auto calc track len.
        TRACK_INTERVAL_LEN = int(TRACK_TRIG_LEN / 2.0) # Max allowed px distance from previous track point
        logging.info("Auto Calculated TRACK_TRIG_LEN=%i and TRACK_INTERVAL_LEN=%i",
                      TRACK_TRIG_LEN, TRACK_INTERVAL_LEN)
    logging.info("Start Stream %s" % cam)
    logging.info("Start Motion Tracking Loop. Ctrl-c Quits ...")
    logging.info("--------------------------------------------")
    tracking = True
    try:
        while tracking:
            image2 = vs.read()
            try:
                grayimage2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
            except:
                continue
            motion_xy = get_motion_track_point(grayimage1, grayimage2)
            grayimage1 = grayimage2  # update for next track
            if motion_xy and start_track:
                track_timer_start = datetime.datetime.now()
                mpoint_start = motion_xy
                prev_mpoint = motion_xy
                max_radius = TRACK_INTERVAL_LEN
                if LOGGING_ON:
                    logging.info("(%i, %i) Track Start: New",
                                 mpoint_start[0], mpoint_start[1])
                if TRACK_HIST_ON: # Reset Tracking History
                    track_hist = [mpoint_start]
                start_track = False
            elif motion_xy:
                mpoint2 = motion_xy
                track_length = track_motion_distance(mpoint_start, mpoint2)
                if TRACK_HIST_ON:
                    track_hist.append(mpoint2)  # Append current mpoint to track history
                if GUI_ON and CIRCLE_ON:
                    cv2.circle(image2,
                               mpoint2,
                               CIRCLE_SIZE,
                               LINE_COLOR,
                               LINE_THICKNESS)
                if track_length <= max_radius:
                    max_radius = track_length + TRACK_INTERVAL_LEN
                else:
                    # ignore out of range points and reset start point
                    mpoint_start = mpoint2
                    if LOGGING_ON:
                        logging.info("(%i, %i) Track Reset: Radius %i Exceeds %i",
                        mpoint2[0], mpoint2[1], track_length, max_radius)
                    start_track = True
                    continue
                if track_length > TRACK_TRIG_LEN:
                    # This was a valid track
                    if LOGGING_ON:
                        logging.info("(%i, %i) Track End: Length %i GT %i TRACK_TRIG_LEN px",
                                     mpoint2[0], mpoint2[1], track_length, TRACK_TRIG_LEN)
                    filename = get_image_name(IM_DIR, IM_PREFIX)
                    logging.info("Saving %s", filename)
                    # Resize image before saving ..
                    if CIRCLE_ON:  # Put Circle on last motion xy before saving image
                        if TRACK_HIST_ON:
                            for point in track_hist:
                                cv2.circle(image2,
                                           point,
                                           CIRCLE_SIZE,
                                           LINE_COLOR,
                                           LINE_THICKNESS)
                        else:
                            cv2.circle(image2,
                                       mpoint2,
                                       CIRCLE_SIZE,
                                       LINE_COLOR,
                                       LINE_THICKNESS)
                    im_resized = cv2.resize(image2, (int(im_width * IM_BIGGER),
                                                 int(im_height * IM_BIGGER)))
                    cv2.imwrite(filename, im_resized)
                    time.sleep(TRACK_DELAY_SEC)  # Delay before starting another track
                    start_track = True
                else:
                    if LOGGING_ON:
                        logging.info("(%i, %i)", mpoint2[0], mpoint2[1])

            if not start_track and timer_end(track_timer_start, TRACK_TIMEOUT_SEC):
                if LOGGING_ON:
                    logging.info("Track Timeout: GT %i TRACK_TIMEOUT_SEC",
                                 TRACK_TIMEOUT_SEC)
                start_track = True

            if GUI_ON:
                cv2.imshow("MoTrack (q in Window Quits)", image2)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    cv2.destroyAllWindows()

    except KeyboardInterrupt:
        print("")
        logging.info("User Pressed Keyboard ctrl-c")
        logging.info("Exiting %s ver %s", PROG_NAME, PROG_VERSION)
        logging.info("Stop Stream Thread: %s", cam)
        logging.info("Wait ...")
        vs.stop()
        sys.exit(0)
