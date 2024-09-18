#!/bin/bash

xhost +local:docker
docker run -it \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    eu-robin-cmd-generator \
    python3 run.py --league wp2
