import os

import cv2
import numpy as np
import time
import mediapipe as mp
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from main2 import detectHandsLandmarks

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
all_hand_landmarks = list()

Y_VALUES = set(range(81, 256))
CR_VALUES = set(range(86, 135))
CB_VALUES = set(range(136, 180))


def process_landmarks(results):
    xs = []
    nums = []
    for hand_landmarks in results.multi_hand_landmarks:
        landmarks = {}
        i = 1
        take_first = True
        for landmark in hand_landmarks.landmark:
            if take_first:
                xs.append(landmark.x)
                if len(nums) == 0:
                    nums.append(0)
                else:
                    nums.append(nums[-1] + 1)
                take_first = False
            landmarks[i] = landmark
            i += 1
        all_hand_landmarks.append(landmarks)


def process_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2YCR_CB)
    for i in range(len(frame)):
        for j in range(len(frame[i])):
            # print(f'frame[{i}][{j}] = {frame[i][j]}', end=' ')
            if frame[i][j][0] in Y_VALUES and frame[i][j][1] in CR_VALUES and frame[i][j][2] in CB_VALUES:
                frame[i][j] = [255, 255, 255]
            else:
                frame[i][j] = [0, 0, 0]
        # print()
    # print(frame)
    return frame


def read_data_from_camera(time1, detect_landmarks: bool = False) -> (bool, bool, int):  # (ok, interrupt, time1, )
    ok, frame = camera_video.read()
    if not ok:
        return False, False, None
    frame = cv2.flip(frame, 1)
    time2 = time.time()
    if detect_landmarks:
        frame, results = detectHandsLandmarks(frame, hands_video, display=False)

        if time2 - time1 > 0:
            frames_per_second = 1.0 / (time2 - time1)
            cv2.putText(frame, 'FPS: {}'.format(int(frames_per_second)),
                        (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
    ret, thresh = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_OTSU)
    cv2.imshow('Hands Landmarks Detection', thresh)
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        return True, True, time2
    if k == 115:
        cv2.imwrite(os.path.join(os.path.dirname(__file__), f'saved_images/image{time.strftime("%Y-%m-%d_%H:%M:%S")}.jpg'), frame)
    if detect_landmarks and results.multi_hand_landmarks:
        process_landmarks(results)
    return True, False, time2


if __name__ == '__main__':
    plt.show()
    hands_video = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7,
                                 min_tracking_confidence=0.4)

    camera_video = cv2.VideoCapture(0)
    camera_video.set(3, 960)
    camera_video.set(4, 960)

    cv2.namedWindow('Hands Landmarks Detection', cv2.WINDOW_NORMAL)
    time1 = 0
    num = 0
    while camera_video.isOpened():
        ok, interrupt, time1 = read_data_from_camera(time1)
        if not ok:
            print('not opened')
            continue
        if interrupt:
            break
    # with open('hand_landmarks.txt', 'w') as file:
    #     for hand_landmark in all_hand_landmarks:
    #         file.write("{}".format(hand_landmarks['x']))
    # with open('hand_landmarks.csv', 'w') as file:
    #     file.write("num, ")
    #     for i in range(1, 22):
    #         file.write(f"x_{i}, y_{i}, z_{i}, ")
    #     file.write("\n")
    #     for i in range(len(all_hand_landmarks)):
    #         landmarks = all_hand_landmarks[i]
    #         file.write(f"{i},")
    #         for j in range(1, 22):
    #             file.write("{},{},{}".format(landmarks[j].x, landmarks[j].y, landmarks[j].x))
    #             file.write(',')
    #         file.write('\n')
    camera_video.release()
    cv2.destroyAllWindows()