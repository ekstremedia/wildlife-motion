libcamera-vid \
    --camera 0 \
    --width 1920 \
    --height 1080 \
    --framerate 30 \
    --codec mjpeg \
    --inline \
    -t 0 \
    --listen -o tcp://0.0.0.0:8554
