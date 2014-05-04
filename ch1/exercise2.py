# Unsharp Masking
from PIL import Image
from scipy.ndimage import filters
from numpy import *
from pylab import *

imColor = array(Image.open('../data/Univ2.jpg'))
imGray = array(Image.open('../data/Univ2.jpg').convert('L'))

sigma = 2

blurColor = zeros(imColor.shape)
for i in range(3):
    blurColor[:, :, i] = filters.gaussian_filter(imColor[:, :, i], sigma)
blurColor = uint8(blurColor)

blurGray = filters.gaussian_filter(imGray, sigma)

maskColor = imColor - blurColor
maskGray = imGray - blurGray


def sharpen(image, mask):
    out = zeros(image.shape)
    for channel in range(len(image[0][0])):
        for y in range(len(image)):
            for x in range(len(image[0])):
                out[y][x][channel] = image[y][x][channel] + mask[y][x][channel]
                # print(uint8(out[y][x][channel]))
    return uint8(out)

def sharpenGray(image,mask):
    out = zeros(image.shape)
    for y in range(len(image)):
        for x in range(len(image[0])):
            out[y][x]= image[y][x]+ mask[y][x]
    return uint8(out)


sharpenedColor = sharpen(imColor, maskColor)
sharpenedGray = sharpenGray(imGray, maskGray)

figure()
images = [imColor, blurColor, maskColor, sharpenedColor,
          imGray, blurGray, maskGray, sharpenedGray]

for i in range(len(images)):
    subplot(2, len(images) / 2, i + 1)
    axis('off')
    gray()
    imshow(images[i])

show()