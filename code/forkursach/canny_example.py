import cv2
from matplotlib import pyplot as plt

IMAGES = ['image1.jpg', 'image3.jpg', 'image7.jpg']
CV2_CVT = [cv2.COLOR_BGR2RGB, cv2.COLOR_BGR2GRAY,
           cv2.COLOR_BGR2HSV, cv2.COLOR_BGR2YCR_CB]
TITLES = ['RGB', 'GRAY', 'HSV', 'YCbCr']


def canny_wrapper(img, cv2_cvt):
    img_cvt = cv2.cvtColor(img, cv2_cvt)
    return cv2.Canny(img_cvt, 100, 200)


def add_image_to_plot(fname, axes):
    img = cv2.imread(fname)
    img_blur = cv2.GaussianBlur(img, (5, 5), 2)
    axes[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    axes[0].set_title('Изображение')
    for i, ax in enumerate(axes[1:]):
        ax.imshow(canny_wrapper(img_blur, CV2_CVT[i]),
                  cmap='gray')
        ax.set_title(TITLES[i])


def union_images():
    fig, axes = plt.subplots(len(IMAGES), 5)
    fig.set_figwidth(15)
    fig.set_figheight(11)
    for i, image_fname in enumerate(IMAGES):
        add_image_to_plot(image_fname, axes[i])

    axes = axes.flatten()
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
    plt.show()
    fig.savefig('canny_ex.png')


def plot_images(img_name):
    fig, axes = plt.subplots(2, 2)
    fig.set_figwidth(10)
    fig.set_figheight(10)
    axes = axes.flatten()
    img = cv2.imread(img_name)
    img_blur = cv2.GaussianBlur(img, (5, 5), 2)
    for i, ax in enumerate(axes):
        ax.imshow(canny_wrapper(img_blur, CV2_CVT[i]),
                  cmap='gray')
        ax.set_title(TITLES[i])
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
    plt.show()
    fig.savefig(f'canny_{img_name.split(".")[0]}.png')


if __name__ == '__main__':
    for image in IMAGES:
        plot_images(image)
