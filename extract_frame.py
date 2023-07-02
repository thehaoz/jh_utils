"""
Frame extraction module

DESCRIPTION
This module provides a simple frame extraction function: ``extract_frames`` that allows
you to extract frames from multiple video files at once. 

USAGE

    python extract_frame.py

    # edit the vid_info list to include the video files you want to extract frames from.
    # vid_dir  - Directory where the video files are located
    # vid_info - State video file name, seek time, skip time, process time 
            {
                "vid_file": "cam8.mp4",
                "seek": 0,  
                "skip": 24,
                "process_time": 0
            },
    # seek time is the time in seconds to start extracting frames from
    # skip time is the number of frames to skip before extracting the next frame
    # process time is the time in seconds to stop extracting frames from the video file
"""

import cv2
import threading
import os
import errno
import time


def mkdir_if_missing(dirname):
    """Creates dirname if it is missing."""
    if not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

def extract_frames(vid_file, skip, seek=0, process_time=0):
    save_counter = 0
    counter = 0
    if os.path.isfile(vid_file):
        fname, ext = os.path.splitext(os.path.basename(vid_file))
        dirname = os.path.dirname(vid_file)
        save_dir = os.path.join(dirname, fname)
        mkdir_if_missing(save_dir)

        cap = cv2.VideoCapture(vid_file)
        cap.set(cv2.CAP_PROP_POS_MSEC, seek*1000)
        if (cap.isOpened()== False):
            print("Error opening video file")
        start = time.time()
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                if (counter + 1) % skip == 0:
                    cv2.imwrite(os.path.join(save_dir, f"{fname}_frame{save_counter}.jpg"), frame)
                    save_counter += 1
                if process_time > 0:
                    if (time.time() - start) > process_time:
                        break
                counter += 1
            else:
                break


    else:
        raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), vid_file)

if __name__ == "__main__":
    vid_directory = "<dir here>"
    vid_info = [
        {
        "vid_file": "cam8.mp4",
        "seek": 0,
        "skip": 24,
        "process_time": 0
        },

    ]
    threads = list()
    for f in vid_info:
        fname = os.path.join(vid_directory, f["vid_file"])
        print(f"extracting {fname}")
        f["vid_file"] = fname
        extract = threading.Thread(target=extract_frames, kwargs=f)
        threads.append(extract)
        extract.start()

    for t in threads:
        t.join()

