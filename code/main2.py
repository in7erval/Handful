import cv2
import numpy as np
from time import time
import mediapipe as mp
import matplotlib.pyplot as plt

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


def detectHandsLandmarks(image, hands, display=True):
    output_image = image.copy()
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    ingHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image=output_image,
                                      landmark_list=hand_landmarks,
                                      connections=mp_hands.HAND_CONNECTIONS)
    if display:
        plt.figure(figsize=[15, 15])
        plt.subplot(121)
        plt.imshow(image[:, :, ::-1])
        plt.title("Original image")
        plt.axis("off")
        plt.subplot(122)
        plt.imshow(output_image[:, :, ::-1])
        plt.title("Processed image")
        plt.axis('off')
        plt.show()
    else:
        return output_image, results


if __name__ == '__main__':
    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.3)
    image = cv2.imread('landmark.png')
    detectHandsLandmarks(image, hands, display=True)
