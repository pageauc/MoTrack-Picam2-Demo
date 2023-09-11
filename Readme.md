# MoTrack 
### Uses python3 and opencv to Track Largest moving object in camera view.

## Introduction
This is just some demo working code to test using picamera2 libcam library with legacy code used in some of my
other projects like speed-camera, pi-timolo, Etc.

## Install or Upgrade motrack demo
***IMPORTANT*** - Update Raspberry Pi Operating System To ensure your system is up-to-date run
In SSH or Terminal Session run commands below below

    sudo apt update
    sudo apt upgrade

#### Step 1
Select copy button on right of Github command box Below  
or Alternatively with mouse left button highlight curl command in code box below. Right click mouse in **highlighted** area and Copy.     

#### Step 2
On RPI putty SSH or Terminal session right click, select paste then Enter to download and run install.sh script.

    curl -L https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/install.sh | bash

## Run Dem in putty SSH or Terminal session

    cd ~/motrack
    ./motrack.py

## Edit Settings per comments

    nano config.py

To exit nano and save changes press

    ctrl-x y

## To run Web Server in background

    ./webserver.sh start

Access webserver with a web browser at provided URL and port

# For More Info See

    See https://github.com/pageauc/MoTrack-Picam2-Demo


Regards Claude....
