# Unsharp Masking
from PIL import Image
from scipy.ndimage import filters
from numpy import *
from pylab import *

imColor = array(Image.open('../data/empire.jpg'))
imGray = array(Image.open('../data/empire.jpg').convert('L'))

sigma = 5

blurColor = zeros(imColor.shape)
for i in range(3):
    blurColor[:, :, i] = filters.gaussian_filter(imColor[:, :, i], sigma)
blurColor = uint8(blurColor)

blurGray = filters.gaussian_filter(imGray, sigma)

maskColor = imColor - blurColor
maskGray = imGray - blurGray


def sharpen(image, mask):
    out = zeros(image.shape)
    threshold = 0.1
    for channel in range(len(image[0][0])):
        for y in range(len(image)):
            for x in range(len(image[0])):
                ratio = mask[y][x][channel]  # / image[x][y][channel]
                print(x, y, ratio)
                # if ratio > threshold:
                # out[x][y][channel] = mask[x][y][channel] + image[x][y][channel]
                #         else:
                #             out[x][y][channel] = image[x][y][channel]
    return out


sharpenedColor = sharpen(imColor, maskColor)

figure()
images = [imColor, blurColor, maskColor,
          imGray, blurGray, maskGray]

for i in range(len(images)):
    subplot(2, len(images) / 2, i + 1)
    axis('off')
    gray()
    imshow(images[i])

show()