import cv2


def to_ycbcr():
    img = cv2.imread('FG_result.png')
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    cv2.imwrite('ycbcr_example.png', img_hsv)


LOWER_YCr_Cb1, UPPER_YCr_Cb1 = (79, 89, 134), \
                               (255, 134, 179)
LOWER_YCr_Cb2, UPPER_YCr_Cb2 = (0, 77, 133), \
                               (255, 127, 173)
INPUT_TO_OUTPUT = {'image3.jpg': ['ycbcr_del1_1.png', 'ycbcr_del1_2.png'],
                   'image7.jpg': ['ycbcr_del2_1.png', 'ycbcr_del2_2.png']}


def YCrCb_skin_detection_mask(image, ex: int):
    img_YCrCb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
    img_YCrCb = cv2.GaussianBlur(img_YCrCb, (5, 5), 5)
    if ex == 1:
        skinMask = cv2.inRange(img_YCrCb, LOWER_YCr_Cb1, UPPER_YCr_Cb1)
    else:
        skinMask = cv2.inRange(img_YCrCb, LOWER_YCr_Cb2, UPPER_YCr_Cb2)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    skinMask = cv2.erode(skinMask, kernel, iterations=3)
    skinMask = cv2.dilate(skinMask, kernel, iterations=3)
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
    return skinMask


if __name__ == '__main__':
    for filename, outputs in INPUT_TO_OUTPUT.items():
        img = cv2.imread(filename)
        for i, output in enumerate(outputs):
            ycrcb_mask = YCrCb_skin_detection_mask(img, i)
            image_skin = cv2.bitwise_and(img, img, mask=ycrcb_mask)
            cv2.imwrite(output, image_skin)
