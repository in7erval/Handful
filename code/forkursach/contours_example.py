import cv2


def process_image(image):
    blurred = cv2.GaussianBlur(image, (3, 3), 3)
    _, thresh1 = cv2.threshold(blurred, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh1


def find_contours_otsu(filename: str, with_processing: bool = False):
    img = cv2.imread(filename)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image_to_contours = process_image(img_gray) if with_processing else img_gray
    contours, hierarchy = cv2.findContours(image_to_contours.copy(),
                    cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print(f'Contours count = {len(contours)}')
    cnt = max(contours, key=lambda x: cv2.contourArea(x))  # находим контур с максимальной площадью
    print(f'Contour area = {cv2.contourArea(cnt)}')
    print(f'Points of contour count = {len(cnt)}')
    cv2.drawContours(img, [cnt], -1, (0, 255, 0), 3)
    cv2.imwrite('contours_otsu_' + ('processing_' if with_processing else '')
                + 'example.png', img)


if __name__ == '__main__':
    find_contours_otsu('image1.jpg')
    find_contours_otsu('image1.jpg', with_processing=True)
