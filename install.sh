#!/bin/bash
echo "MoTeack  Install  written by Claude Pageau"
echo "INFO  : Create motrack Folders ..."
cd ~
mkdir -p motrack
cd motrack

echo "INFO  : Download Project Files ..."
wget -O motrack.py -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/motrack.py
wget -O webserver.py -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/webserver.py
wget -O webserver.sh -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/webserver.sh
if [ -f config.py ]; then     # check if local file exists.
    wget -O config.py.new -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/config.py.new
else
    wget -O config.py -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/config.py
fi
wget -O streampilegacycam.py -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/streampilegacycam.py
wget -O streampilibcam.py -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/streampilibcam.py
wget -O streamwebcam.py -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/streamwebcam.py
wget -O readme.md -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/readme.md

chmod +x motrack.py webserver.py webserver.sh

echo "INFO  : Install Dependencies ...."
sudo apt install -yq python3-opencv

echo "
                    INSTRUCTIONS
                    ============
To Run Demo in SSH or Terminal session Default is USB Webcam
Edit config.py CAMERA setting for RPI Legacy, Libcam or RTSP IP Camera

    cd ~/motrack
    ./motrack.py

To Change Settings

    nano config.py

To exit nano and save settings press

    ctrl-x y

To run Web Server in background

    ./webserver.sh start

Access webserver wirh a web browser at peovided URL

Form More Info See https://github.com/pageauc/MoTrack-Picam2-Demo

"
