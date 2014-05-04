from PIL import Image
from numpy import *
from pylab import *
from scipy.ndimage import filters
from scipy import misc

images = [misc.lena(), misc.face(), misc.ascent()]


def gaussian(image, sigma):
    out = zeros(image.shape)
    if (isinstance(image[0][0], list)):
        for i in range(3):
            out[:, :, i] = filters.gaussian_filter(image[:, :, i], sigma)
    else:
        out = filters.gaussian_filter(image, sigma)
    return uint8(out)


figure()
gray()
for i in range(len(images)):
    subplot(len(images), 2, 2 * i + 1)
    axis('off')
    imshow(images[i])

    sigma = 20
    quotientImage = images[i] / gaussian(images[i], sigma)
    subplot(len(images), 2, 2 * i + 2)
    axis('off')
    imshow(quotientImage)

show()