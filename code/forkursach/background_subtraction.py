import os

import cv2
import numpy as np
from PIL import Image, ImageChops
import math

def background_subtraction():
    bg = cv2.imread('BG_result.png')
    fg = cv2.imread('FG_result.png')
    # diff = cv2.absdiff(fg, bg)
    # mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    # th = 30
    # imask = mask > th
    # canvas = np.zeros_like(fg, np.uint8)
    # canvas[imask] = fg[imask]
    # cv2.imwrite('result.png', canvas)

    def difference(pixel1, pixel2):
        return math.sqrt((int(pixel1[0]) - int(pixel2[0]))**2 +
                         (int(pixel1[1]) - int(pixel2[1]))**2 +
                         (int(pixel1[2]) - int(pixel2[2]))**2)

    THRESHOLD = 30
    mask = np.zeros_like(bg, np.uint8)
    for i in range(len(bg)):
        for j in range(len(bg[i])):
            mask[i][j] = fg[i][j] if difference(bg[i][j], fg[i][j]) > THRESHOLD else (0, 0, 0)
    cv2.imwrite('result1.png', mask)



if __name__ == '__main__':
    background_subtraction()

