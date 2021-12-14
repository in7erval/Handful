import numpy as np
import cv2
import matplotlib.pyplot as plt


def get_min_max(image_flatten: np.ndarray) -> tuple:
    min_pix, max_pix = image_flatten[0], image_flatten[0]
    for pixel in image_flatten:
        if pixel < min_pix:
            min_pix = pixel
        if pixel > max_pix:
            max_pix = pixel
    return min_pix, max_pix


def create_histogram(image_flatten: np.ndarray, size: int, min_pix: int) -> np.array:
    hist = np.zeros(size)
    for pixel in image_flatten:
        hist[pixel - min_pix] += 1
    return hist


def otsu_threshold(image: np.ndarray):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_gray_flatten = img_gray.flatten()
    min_pixel, max_pixel = get_min_max(img_gray_flatten)
    size = max_pixel - min_pixel + 1
    histogram = create_histogram(img_gray_flatten, size, min_pixel)
    m = 0  # сумма высот бинов, домноженных на положение их середины
    n = 0  # сумма высот всех бинов
    for i in range(size):
        m += i * histogram[i]
        n += histogram[i]
    max_sigma = -1  # Максимальное значение межклассовой дисперсии
    threshold = 0  # Порог, соответствующий maxSigma
    alpha1 = 0  # Сумма высот всех бинов для класса 1
    beta1 = 0  # Сумма высот всех бинов для класса 1, домноженных на положение их середины
    for i in range(size - 1):
        alpha1 += i * histogram[i]
        beta1 += histogram[i]
        w1 = float(beta1) / n  # Вероятность класса 1
        w2 = 1 - w1
        a = float(alpha1) / beta1 - float(m - alpha1) / (
                n - beta1)  # a = a1 - a2, где a1, a2 -- средние арифметические для классов 1 и 2
        sigma = w1 * w2 * a * a
        if sigma > max_sigma:
            max_sigma = sigma
            threshold = i
    threshold += min_pixel
    return threshold


def save_histogram(image, fname: str):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).flatten()
    plt.hist(image, 255)
    plt.xlim([0, 255])
    plt.savefig(fname)
    plt.show()


INPUT_TO_OUTPUT = {'image3.jpg':
                       {'histogram': 'histogram_for_3.png',
                        'output': 'otsu_exmpl_for_3.png'},
                   'image7.jpg':
                       {'histogram': 'histogram_for_7.png',
                        'output': 'otsu_exmpl_for_7.png'}
                   }

if __name__ == '__main__':
    for fname, outputs in INPUT_TO_OUTPUT.items():
        image = cv2.imread(fname)
        save_histogram(image, outputs['histogram'])
        thresh = otsu_threshold(image)
        print(f'Threshold = {thresh}')
        ret, img_thresh = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), thresh, 255, cv2.THRESH_BINARY)
        imask = img_thresh == 255
        canvas = np.zeros_like(image, np.uint8)
        canvas[imask] = image[imask]
        cv2.imwrite(outputs['output'], canvas)
