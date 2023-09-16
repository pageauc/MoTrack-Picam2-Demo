# MoTrack 
#### Uses python3 and opencv to Track Largest moving object in camera view (picamera2 libcam, picamera legacy, RTSP IP cam or USB Webcam).

## Introduction
This is just some demo working code to test motion tracking using python picamera2 libcam, picamera legacy Camera,  rtsp IP camera or USB Webcam.
On completion of a successful track an image is saved in ./media/images
Optional tracking history can be displayed on images as contour center point circles or contour rectangles.
Images can be viewed on web browser via provided webserver.py run in foreground or background. 
Program user settings are saved in the config.py file and configcam.py.

Note.
This version isolates camera stream thread logic. This allows easy integration into my other projects since only I can remove old camera related code
and simply add two lines.  PI legacy, Libcam, USB and RTSP IP Cameras can be configured using the CAMERA variable in configcam.py

    from strmcam import strmcam
    
    vs = strmcam()  # start video stream thread
    
    # example implementation
    image = vs.read()
    vs.stop()

## Install or Upgrade
***IMPORTANT*** - Update Raspberry Pi Operating System To ensure your system is up-to-date.
In SSH or Terminal Session run commands below.

    sudo apt update
    sudo apt upgrade

#### Step 1
Select copy icon on right of Github command box below  
or Alternatively with mouse left button highlight curl command in code box below. Right click mouse in **highlighted** area and Copy.     

    curl -L https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/install.sh | bash

#### Step 2
On RPI putty SSH or Terminal session, right click, select paste then Enter to download and run install.sh script.

***NOTE*** If config.py exists it will Not be overwritten. A config.py.new and/or config.cam.py will be created/updated instead.
To update existing config.py perform commands below

    cd ~/motrack
    cp config.py config.py.bak
    cp config.py.new config.py
    cp configcam.py configcam.py.bak
    cp configcam.py.new configcam.py  

## Edit Settings
To review and/or change settings execute command below in SSH or terminal session.
See comments for each variable setting. Ensure camera is installed and working.

    cd ~/motrack
    nano config.py
or    
    nano configcam.py

To exit nano and save changes press

    ctrl-x y

## Run motrack
  Open putty SSH or Terminal session then execute command below.

    cd ~/motrack
    ./motrack.py

If camera is working motion tracking logging information will be displayed.

## WebServer
Webserver.py will display saved motrack images from any network device using a web browser.

#### Foreground
To Run in Foreground open a new SSH or Terminal Session then execute command below.

    ./webserver.py

NOTE browser URL:PORT for accessing MoTrack web page will be displayed.  ctrl-c exits.

#### Background
To Run in Background execute command below in current SSH or Terminal Session. 
Then execute motrack.py in same terminal session per above.

    ./webserver.sh start

Access webserver with a web browser at provided URL and port  eg http://192.168.1.128:8080 or http://rpiname.local:8080

## More Info See

    https://github.com/pageauc/MoTrack-Picam2-Demo


Regards Claude....
