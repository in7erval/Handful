import cv2
import numpy as np


def to_hsv():
    img = cv2.imread('FG_result.png')
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
    cv2.imwrite('hsv_example.png', img_hsv)


LOWER, UPPER = np.array([0, 15, 80], dtype='uint8'), \
               np.array([200, 255, 255], dtype='uint8')

INPUT_TO_OUTPUT = {'image3.jpg': 'hsv_del1.png',
                   'image7.jpg': 'hsv_del2.png'}

def HSV_skin_detection_mask_first(image):
    converted = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted, LOWER, UPPER)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    skinMask = cv2.erode(skinMask, kernel, iterations=2)
    skinMask = cv2.dilate(skinMask, kernel, iterations=2)
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
    return skinMask


if __name__ == '__main__':
    for filename_input, filename_output in INPUT_TO_OUTPUT.items():
        img = cv2.imread(filename_input)
        hsv_mask = HSV_skin_detection_mask_first(img)
        cv2.imwrite(filename_output, cv2.bitwise_and(img, img, mask=hsv_mask))