libcamera-vid \
  --camera 1 \
  --framerate 30 \
  --width 1920 --height 1080 \
  --codec h264 \
  --inline \
  --libav-format h264 \
  -t 10000 \
  -o - | \
ffmpeg \
  -y \
  -i pipe:0 \
  -c copy \
  /var/www/html/test.mp4

