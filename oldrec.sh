#!/bin/bash
DATE=$(date +"%Y%m%d%H%M%S")
DIR="/var/www/html/motion/FFMPEG $(date +"%Y/%m/%d")"
mkdir -p "$DIR"
/usr/bin/libcamera-vid -t 0 --width 1920 --height 1080 --framerate 30 -c:v h264_v4l2m2m --inline -o - | ffmpeg -y -i - -c copy "$DIR/motion$DATE.mp4" &
echo $! > /tmp/libcamera-vid.pid
