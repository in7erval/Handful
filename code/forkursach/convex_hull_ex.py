import math
import time

import numpy as np
import random
from matplotlib import pyplot as plt
import cv2


def process_image(image):
    blurred = cv2.GaussianBlur(image, (3, 3), 3)
    return cv2.threshold(blurred, 0, 255,
                         cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]


def squeeze(array):
    array = array[0] if len(array) == 1 else array
    return [p[0] for p in array] if len(array[0]) == 1 else array


# "очистка" выпуклой оболочки до не больше 7 точек
def clear_convex_hull(hull_index, contour):
    distance_point = lambda p1, p2: math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    hull_index, contour = squeeze(hull_index), squeeze(contour)
    ALPHA = 200
    while True:
        boundary = len(hull_index) - 1
        clean_hull, i = [], 0
        while i < boundary:
            clean_hull.append(hull_index[i])
            while i < boundary and \
                    distance_point(contour[hull_index[i]], contour[hull_index[i + 1]]) < ALPHA:
                i += 1
            i += 1
        if len(clean_hull) > 7:
            ALPHA += 1
        else:
            break
    return np.array(clean_hull[:-1]) if \
        distance_point(contour[clean_hull[0]], contour[clean_hull[-1]]) < ALPHA else \
        np.array(clean_hull)

def draw_lines(image, points, center):
    for point in points:
        cv2.line(image, center, point, (0, 0, 255), 5)

if __name__ == '__main__':
    img = cv2.imread('image1.jpg')
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image_to_contours = process_image(img_gray)
    contours, hierarchy = cv2.findContours(image_to_contours.copy(),
                                           cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = max(contours, key=lambda x: cv2.contourArea(x))  # находим контур с максимальной площадью
    cv2.drawContours(img, [cnt], -1, (0, 255, 0), 2)
    hull = cv2.convexHull(cnt)
    cv2.drawContours(img, [hull], -1, (255, 0, 0), 2)
    hull_index = cv2.convexHull(cnt, returnPoints=False)
    defects = cv2.convexityDefects(cnt, hull_index)
    hull_index = clear_convex_hull(hull_index, cnt)
    M = cv2.moments(cnt)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    draw_lines(img, [cnt[h][0] for h in hull_index], (cX, cY))
    for h in hull_index:
        cv2.circle(img, cnt[h][0], 10, (0, 255, 255), -1)
    for defect in defects:
        # print(defect)
        cv2.circle(img, cnt[defect[0][2]][0], 5, (0, 0, 255), -1)
    cv2.circle(img, (cX, cY), 10, (255, 255, 0), -1)
    (x, y), radius = cv2.minEnclosingCircle(cnt)
    center = (int(x), int(y))
    radius = int(radius)
    cv2.circle(img, center, radius, (0, 255, 0), 2)
    # fit ellipse (blue)
    ellipse = cv2.fitEllipse(cnt)
    cv2.ellipse(img, ellipse, (255, 0, 0), 2)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()
    cv2.imwrite('test.png', img)
