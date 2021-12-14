import dlib
import glob
import cv2
import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import pyautogui as pyg
import shutil

from preparation.constants import DIRECTORY, BOX_FILE


def generate_data():
    # Чистка предыдущих фреймов
    cleanup = True

    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('frame', 1920, 1080)
    cv2.moveWindow("frame", 0, 0)
    cap = cv2.VideoCapture(0)

    # sliding window coordinates
    x1, y1 = 0, 0
    # sliding window size
    window_width = 300  # 140
    window_height = 300

    # save every 4'th image
    skip_frames = 3
    frame_gap = 0

    if cleanup:
        if os.path.exists(DIRECTORY):
            shutil.rmtree(DIRECTORY)
        open(BOX_FILE, 'w').close()
        counter = 0
    elif os.path.exists(BOX_FILE):
        with open(BOX_FILE, 'r') as text_file:
            box_content = text_file.read()
        counter = int(box_content.split(':')[-2].split(',')[-1])
    fr = open(BOX_FILE, 'a')
    if not os.path.exists(DIRECTORY):
        os.mkdir(DIRECTORY)
    initial_wait = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        orig = frame.copy()
        if initial_wait > 60:
            frame_gap += 1
            if x1 + window_width < frame.shape[1]:
                x1 += 4
                time.sleep(0.1)
            elif y1 + window_height + 270 < frame.shape[1]:
                y1 += 80
                x1 = 0
                frame_gap = 0
                initial_wait = 0
            else:
                break
        else:
            initial_wait += 1

        # Save the image every nth frame.
        if frame_gap == skip_frames:
            # Set the image name equal to the counter value
            img_name = str(counter) + '.png'

            # Save the Image in the defined directory
            img_full_name = DIRECTORY + '/' + str(counter) + '.png'
            cv2.imwrite(img_full_name, orig)

            # Save the bounding box coordinates in the text file.
            fr.write('{}:({},{},{},{}),'.format(counter, x1, y1, x1 + window_width, y1 + window_height))

            # Increment the counter
            counter += 1

            # Set the frame_gap back to 0.
            frame_gap = 0

        # Draw the sliding window
        cv2.rectangle(frame, (x1, y1), (x1 + window_width, y1 + window_height), (0, 255, 0), 3)

        # Display the frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    # Release camera and close the file and window
    cap.release()
    cv2.destroyAllWindows()
    fr.close()