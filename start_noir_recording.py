#!/usr/bin/env python3

import sys
import subprocess
import time
import os
import logging
import traceback
import signal
from datetime import datetime

# 1) Set up logging directory and logfile
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOGFILE = os.path.join(LOG_DIR, "noir.log")

# 2) Configure the logging
logging.basicConfig(
    filename=LOGFILE,
    filemode="a",  # append to the file
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO
)

PIDFILE = "/tmp/noir_libcamera.pid"

def generate_filename():
    """
    Generate a date-based folder path in /var/www/html/motion/YYYY/MM/DD/
    and a filename noir_HH_MM_SS.mp4
    """
    now = datetime.now()

    # Build date-based folder path
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")

    folder_path = f"/var/www/html/motion/{year}/{month}/{day}"

    # Create folders if they don't exist
    try:
        os.makedirs(folder_path, exist_ok=True)
        logging.info(f"Ensured directory exists: {folder_path}")
    except Exception as e:
        logging.error("Failed to create directories: %s", str(e))
        logging.error(traceback.format_exc())

    # Create a filename with the HH_MM_SS time stamp
    timestamp = now.strftime("%H_%M_%S")
    filename = f"noir_{timestamp}.mp4"

    # Combine folder path and file name
    output_path = os.path.join(folder_path, filename)
    logging.info(f"Generated output file path: {output_path}")

    return output_path

def start_recording():
    """
    Start libcamera-vid in the background, saving directly to MP4 using --codec libav.
    Write the PID to /tmp/noir_libcamera.pid so we can stop it later.
    """
    logging.info("start_recording() called")

    output_file = generate_filename()

    # Example command using libcamera-vid for an MP4 output:
    # libcamera-vid --camera 1 --codec libav --width 1920 --height 1280 -o output.mp4
    # (Adjust as needed for your camera index/resolution/etc.)
    libcamera_cmd = [
        "libcamera-vid",
        "--camera", "1",
        "--codec", "libav",
        "--width", "1920",
        "--height", "1080",
        "-t", "0", 
        "-o", output_file
    ]

    logging.info(f"libcamera-vid command: {' '.join(libcamera_cmd)}")

    try:
        # Run libcamera-vid in the background, discard stdout/stderr
        process = subprocess.Popen(libcamera_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logging.info(f"libcamera-vid started, PID={process.pid}")

        # Save the PID so we can stop it later
        with open(PIDFILE, "w") as f:
            f.write(str(process.pid))
        logging.info(f"PID file created: {PIDFILE}")

    except Exception as e:
        logging.error("Error launching libcamera-vid: %s", str(e))
        logging.error(traceback.format_exc())

def stop_recording():
    """
    Wait 2 seconds after motion ends, then send SIGINT (like Ctrl+C)
    to libcamera-vid. Remove the PID file after it exits.
    """
    logging.info("stop_recording() called, waiting 2 seconds before stopping libcamera-vid")
    time.sleep(2)

    if os.path.exists(PIDFILE):
        try:
            with open(PIDFILE, "r") as f:
                pid = int(f.read().strip())

            logging.info(f"Sending SIGINT to libcamera-vid process with PID={pid}")
            # Send SIGINT (same signal as Ctrl+C)
            os.kill(pid, signal.SIGINT)

            # Optionally wait a little for the process to exit
            time.sleep(3)

            # Check if it's still running, and if so, try SIGTERM or SIGKILL
            # If you want to keep it simple, you can skip this check.
            try:
                # os.kill(pid, 0) will raise an OSError if pid doesn't exist
                os.kill(pid, 0)
                # If no exception, process is still running:
                logging.info("Process still alive, sending SIGKILL...")
                os.kill(pid, signal.SIGKILL)
            except OSError:
                # The process is gone; success
                logging.info("Process exited gracefully.")

            # Remove the PID file
            os.remove(PIDFILE)
            logging.info(f"PID file removed: {PIDFILE}")

        except Exception as e:
            logging.error("Error stopping libcamera-vid: %s", str(e))
            logging.error(traceback.format_exc())
    else:
        logging.warning(f"PID file not found, cannot stop libcamera-vid: {PIDFILE}")
        
if __name__ == "__main__":
    """
    Script usage:
      ./start_noir_recording.py start
      ./start_noir_recording.py stop
    """
    if len(sys.argv) < 2:
        logging.error("Usage: start_noir_recording.py [start|stop]")
        print("Usage: start_noir_recording.py [start|stop]")
        sys.exit(1)

    action = sys.argv[1].lower()
    logging.info(f"Script called with action: {action}")

    if action == "start":
        start_recording()
    elif action == "stop":
        stop_recording()
    else:
        logging.error("Unknown argument: %s", action)
        print("Unknown argument:", action)
        sys.exit(1)

