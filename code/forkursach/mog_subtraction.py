import cv2
import numpy as np

subtractor = cv2.createBackgroundSubtractorMOG2()
capture = cv2.VideoCapture(0)

def remove_bg(frame, fgMask):
    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgMask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res

def learn_and_capture(is_learn=False, is_capture=False):
    # обучение на фоне
    while True:
        ret, frame = capture.read()
        while frame is None:
            print("Try to read")
            ret, frame = capture.read()
        if is_learn:
            fgMask = subtractor.apply(frame)
            cv2.rectangle(frame, (10, 2), (100, 20), (255, 255, 255), -1)
            # cv2.imshow('Frame', frame)
            removed_bg = remove_bg(frame, fgMask)
            cv2.imshow('result', removed_bg)
        elif is_capture:
            cv2.imshow('Capture frame. Press esc', frame)
        else:
            raise RuntimeError('Illegal arguments in function!')
        keyboard = cv2.waitKey(500)
        if keyboard == 'q' or keyboard == 27:
            break
    if is_capture:
        return frame

if __name__ == '__main__':
    learn_and_capture(is_learn=True)
    frame = learn_and_capture(is_capture=True)
    fgMask = subtractor.apply(frame)
    removed_bg = remove_bg(frame, fgMask)
    cv2.imwrite('mog_result.png', removed_bg)