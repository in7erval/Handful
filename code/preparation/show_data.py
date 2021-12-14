import cv2
import numpy as np
from matplotlib import pyplot as plt


def show_images(data: dict):
    no_of_samples = 10

    keys = list(data.keys())
    np.random.shuffle(keys)
    # Extract the subset of boxes
    # subset = data[][:no_of_samples ]

    cols = 5

    # Given the number of samples to display, what's the number of rows required.
    rows = int(np.ceil(no_of_samples / cols))

    # Set the figure size
    plt.figure(figsize=(cols * cols, rows * cols))

    # Loop for each class
    for i in range(no_of_samples):
        index_show = keys[i]
        # Extract the bonding box coordinates
        d_box = data[index_show][1][0]
        left, top, right, bottom = d_box.left(), d_box.top(), d_box.right(), d_box.bottom()
        print(f"Get left({left}), top({top}), right({right}), bottom({bottom}) coordinate for {index_show}")
        # Get the image
        image = data[index_show][0]

        # Draw rectangle on the detected hand
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 3)

        # Display the image
        plt.subplot(rows, cols, i + 1)
        plt.imshow(image[:, :, ::-1])
        plt.axis('off')
    plt.show()
