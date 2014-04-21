from PIL import Image
from numpy import *
from scipy.ndimage import filters
from pylab import *

# Dx and Dy are discrete approximation matrix convolutions of the original image data points with the respective kernels

# I'x = I * Dx // image partial derivative in the x direction
#I'y = I * Dy // partial derivative in the y direction

#Sobel derivative filter
#
#      [-1  0  1]        [-1 -2 -1]
# Dx = [-2  0  2]   Dy = [ 0  0  0]
#      [-1  0  1]        [ 1  2  1]

#Prewitt derivative filter
#
#      [-1  0  1]        [-1 -1 -1]
# Dx = [-1  0  1]   Dy = [ 0  0  0]
#      [-1  0  1]        [ 1  1  1]


#sobel example
im = array(Image.open('data/empire.jpg').convert('L'))
imx = zeros(im.shape)
imy = zeros(im.shape)

filters.sobel(im, 1, imx)
filters.sobel(im, 0, imy)

magnitude = sqrt(imx ** 2 + imy ** 2)
figure()
gray()

subplot(1, 4, 1)
imshow(im)

subplot(1, 4, 2)
imshow(imx)

subplot(1, 4, 3)
imshow(imy)

subplot(1, 4, 4)
imshow(magnitude)

show()

#guassian derivatives
sigmas = [2, 5, 10]

figure()
gray()
for rowStart in [1, 5, 9]:
    subplot(3, 4, rowStart)
    imshow(im)

figures = []
for idx, sigma in enumerate(sigmas):
    figures.append(zeros(im.shape))
    filters.gaussian_filter(im, (sigma, sigma), (0, 1), figures[-1])
    subplot(3,4,2 + idx)
    imshow(figures[-1])

    figures.append(zeros(im.shape))
    filters.gaussian_filter(im, (sigma, sigma), (1, 0), figures[-1])
    subplot(3,4,6 + idx)
    imshow(figures[-1])

    subplot(3,4,10 + idx)
    figures.append(sqrt(figures[-2]** 2 + figures[-1]** 2))
    imshow(figures[-1])

show()