#!/bin/bash
echo "MoTrack  Install  written by Claude Pageau"
echo "INFO  : Create motrack Folders ..."
cd ~
mkdir -p motrack
cd motrack

echo "INFO  : Download Project Files ..."
wget -O motrack.py -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/motrack.py
wget -O webserver.py -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/webserver.py
wget -O webserver.sh -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/webserver.sh

if [ -f config.py ]; then     # check if local file exists.
    wget -O config.py.new -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/config.py
else
    wget -O config.py -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/config.py
fi
if [ -f configcam.py ]; then     # check if local file exists.
    wget -O configcam.py.new -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/configcam.py
else
    wget -O configcam.py -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/configcam.py
fi

wget -O strmcam.py -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/strmcam.py
wget -O strmpilegcam.py -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/strmpilegcam.py
wget -O strmusbipcam.py -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/strmusbipcam.py
wget -O strmpilibcam.py -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/strmpilibcam.py
wget -O Readme.md -q --show-progress https://raw.github.com/pageauc/MoTrack-Picam2-Demo/master/Readme.md

chmod +x motrack.py webserver.py webserver.sh

echo "INFO  : Install Dependencies ...."
sudo apt install -yq python3-opencv

echo "
                    INSTRUCTIONS
                    ============
RUN DEMO
========
In SSH or Terminal session Default is USB Webcam
Edit config.py CAMERA setting for RPI Legacy, Libcam or RTSP IP Camera

    cd ~/motrack
    ./motrack.py

EDIT SETTINGS
=============

    nano config.py

To exit and save settings. In nano press

    ctrl-x then y

RUN WEBSERVER
=============

Run Web in Foreground open a new terminal (Displays browser URL)

    ./webserver.py

Run in Background in existing terminal

    ./webserver.sh start

Access webserver wirh a web browser at URL per Foreground command.

Form More Info See https://github.com/pageauc/MoTrack-Picam2-Demo

"
