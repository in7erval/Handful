import math

import cv2
import numpy as np
from time import time
import mediapipe as mp
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from main2 import detectHandsLandmarks

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

NUM_DOTS = 21
fig = plt.figure(figsize=(15, 8))
axes = fig.subplots(3, 7)
all_axes = list()
for axs in axes:
    for ax in axs:
        all_axes.append(ax)
lines = {"x": dict(), "y": dict(), "z": dict()}
for i in range(NUM_DOTS):
    lines["x"][i] = all_axes[i].plot([], [], 'r', animated=True)[0]
for i in range(NUM_DOTS):
    lines["y"][i] = all_axes[i].plot([], [], 'g', animated=True)[0]
for i in range(NUM_DOTS):
    lines["z"][i] = all_axes[i].plot([], [], 'b', animated=True)[0]
camera_video = cv2.VideoCapture(0)
camera_video.set(3, 1280)
camera_video.set(4, 960)
hands_video = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7,
                             min_tracking_confidence=0.4)

nums = []
xs = [[] for i in range(NUM_DOTS)]
ys = [[] for i in range(NUM_DOTS)]
zs = [[] for i in range(NUM_DOTS)]


def set_all_lines():
    for i in range(NUM_DOTS):
        lines['x'][i].set_data(nums, xs[i])
        lines['y'][i].set_data(nums, ys[i])
        lines['z'][i].set_data(nums, zs[i])


def lines2tuple():
    t = list()
    for i in range(NUM_DOTS):
        t.append(lines['x'][i])
        t.append(lines['y'][i])
        t.append(lines['z'][i])
    return tuple(t)


def init():
    for ax in all_axes:
        ax.set_xlim(0, 500)
        ax.set_ylim(0, 1)
    set_all_lines()
    return lines2tuple()


def read_data_from_camera(i):
    ok, frame = camera_video.read()
    if ok:
        frame = cv2.flip(frame, 1)
        frame, results = detectHandsLandmarks(frame, hands_video, display=False)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if len(hand_landmarks.landmark) == NUM_DOTS:
                    for i in range(len(hand_landmarks.landmark)):
                        landmark = hand_landmarks.landmark[i]
                        xs[i].append(landmark.x)
                        ys[i].append(landmark.y)
                        zs[i].append(landmark.z)
                    if len(nums) == 0:
                        nums.append(0)
                    else:
                        nums.append(nums[-1] + 1)
    set_all_lines()
    return lines2tuple()


ani = animation.FuncAnimation(fig, read_data_from_camera, init_func=init,
                              frames=1000, interval=30, blit=True, repeat=False)
plt.show()
