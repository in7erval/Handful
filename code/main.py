from preparation.constants import DIRECTORY, BOX_FILE, GENERATE_DATA, PREPARE_DATA, SHOW_IMAGES, TRAIN_DETECTOR, \
    TEST_DETECTOR_LIVE
from preparation.generate_data import generate_data
from preparation.preparating_data import prepare_data
from preparation.show_data import show_images
from preparation.test_detector import test_detector
from preparation.train_detector import train_detector_and_save

if __name__ == '__main__':
    if GENERATE_DATA:
        print("-- DATA GENERATION --")
        generate_data()
    if PREPARE_DATA:
        print("-- DATA PREPARATION --")
        data = prepare_data()
        if SHOW_IMAGES:
            print("-- SHOW IMAGES --")
            show_images(data)
        if TRAIN_DETECTOR:
            print("-- DETECTOR TRAINING --")
            train_detector_and_save(data)
    if TEST_DETECTOR_LIVE:
        print("-- TEST DETECTOR --")
        test_detector()
