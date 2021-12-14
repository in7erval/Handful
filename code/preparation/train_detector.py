import time

import dlib

from preparation.constants import DETECTOR_FILENAME


def train_detector_and_save(data: dict):
    # This is the percentage of data we will use to train
    # The rest will be used for testing
    percent = 0.8

    # How many examples make 80%.
    split = int(len(data) * percent)

    # Separate the images and bounding boxes in different lists.
    images = [tuple_value[0] for tuple_value in data.values()]
    bounding_boxes = [tuple_value[1] for tuple_value in data.values()]

    # Initialize object detector Options
    options = dlib.simple_object_detector_training_options()

    # I'm disabling the horizontal flipping, becauase it confuses the detector if you're training on few examples
    # By doing this the detector will only detect left or right hand (whichever you trained on).
    options.add_left_right_image_flips = False

    # Set the c parameter of SVM equal to 5
    # A bigger C encourages the model to better fit the training data, it can lead to overfitting.
    # So set an optimal C value via trail and error.
    options.C = 5

    # Note the start time before training.
    st = time.time()

    # You can start the training now
    print("train splitted")
    detector = dlib.train_simple_object_detector(images[:split], bounding_boxes[:split], options)

    # Print the Total time taken to train the detector
    print('Training Completed, Total Time taken: {:.2f} seconds'.format(time.time() - st))

    detector.save(DETECTOR_FILENAME)

    win_det = dlib.image_window()
    win_det.set_image(detector)

    print("Training Metrics: {}".format(
        dlib.test_simple_object_detector(images[:split], bounding_boxes[:split], detector)))

    print("train all")
    detector = dlib.train_simple_object_detector(images, bounding_boxes, options)
    detector.save(DETECTOR_FILENAME)
