import os
import time

import cv2
import dlib

from preparation.constants import DETECTOR_FILENAME


def test_detector():
    # Load our trained detector
    detector = dlib.simple_object_detector(os.path.join(os.path.join(os.getcwd(), 'preparation'), DETECTOR_FILENAME))

    # Set the window name
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

    # Initialize webcam
    cap = cv2.VideoCapture(0)

    # Setting the downscaling size, for faster detection
    # If you're not getting any detections then you can set this to 1
    scale_factor = 2.0

    # Initially the size of the hand and its center x point will be 0
    size, center_x = 0, 0

    # Initialize these variables for calculating FPS
    fps = 0
    frame_counter = 0
    start_time = time.time()

    # Set the while loop
    while True:
        # Read frame by frame
        ret, frame = cap.read()
        while not ret:
            print('test read')
            ret, frame = cap.read()

        # Laterally flip the frame
        frame = cv2.flip(frame, 1)

        # Calculate the Average FPS
        frame_counter += 1
        fps = (frame_counter / (time.time() - start_time))

        # Create a clean copy of the frame
        copy = frame.copy()

        # Downsize the frame.
        new_width = int(frame.shape[1] / scale_factor)
        new_height = int(frame.shape[0] / scale_factor)
        resized_frame = cv2.resize(copy, (new_width, new_height))

        # Detect with detector
        detections = detector(resized_frame)

        # Loop for each detection.
        for detection in detections:
            # Since we downscaled the image we will need to resacle the coordinates according to the original image.
            x1 = int(detection.left() * scale_factor)
            y1 = int(detection.top() * scale_factor)
            x2 = int(detection.right() * scale_factor)
            y2 = int(detection.bottom() * scale_factor)

            # Draw the bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, 'Hand Detected', (x1, y2 + 20), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 255), 2)

            # Calculate size of the hand.
            size = int((x2 - x1) * (y2 - y1))

            # Extract the center of the hand on x-axis.
            center_x = x2 - x1 // 2

        # Display FPS and size of hand
        cv2.putText(frame, 'FPS: {:.2f}'.format(fps), (20, 20), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 255), 2)

        # This information is useful for when you'll be building hand gesture applications
        cv2.putText(frame, 'Center: {}'.format(center_x), (540, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (233, 100, 25))
        cv2.putText(frame, 'size: {}'.format(size), (540, 40), cv2.FONT_HERSHEY_COMPLEX, 0.5, (233, 100, 25))

        # Display the image
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and destroy all windows
    cap.release()
    cv2.destroyAllWindows()