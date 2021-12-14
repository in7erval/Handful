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


def prepare_data() -> dict:

    # In this dictionary our images and annotations will be stored.
    data = {}

    # Get the indexes of all images.
    image_indexes = [int(img_name.split('.')[0]) for img_name in os.listdir(DIRECTORY)]
    print(f"Get image indexes: [{image_indexes[:5]}, ...]")
    # Shuffle the indexes to have random train/test split later on.
    np.random.shuffle(image_indexes)
    print(f"Shuffle image indexes: [{image_indexes[:5]}, ...]")
    # Open and read the content of the boxes.txt file
    f = open(BOX_FILE, "r")
    box_content = f.read()

    # Convert the bounding boxes to dictionary in the format `index: (x1,y1,x2,y2)` ...
    box_dict = eval('{' + box_content + '}')
    print(f"Get boxes dictionary: (sample for 0) {box_dict[0]}")

    # Close the file
    f.close()

    # Loop over all indexes
    for index in image_indexes:
        # Read the image in memmory and append it to the list
        img = cv2.imread(os.path.join(DIRECTORY, str(index) + '.png'))

        # Read the associated bounding_box
        bounding_box = box_dict[index]

        # Convert the bounding box to dlib format
        x1, y1, x2, y2 = bounding_box
        dlib_box = [dlib.rectangle(left=x1, top=y1, right=x2, bottom=y2)]

        # Store the image and the box together
        data[index] = (img, dlib_box)

    print(f"Data for dlib prepared: (sample for 0) {data[0]}")
    return data



