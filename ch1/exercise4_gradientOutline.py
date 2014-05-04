from PIL import Image
from numpy import *
from scipy.ndimage import filters
from pylab import *

def simpleOutline(image):
    imx = zeros(image.shape)
    imy = zeros(image.shape)
    filters.sobel(im,1,imx)
    filters.sobel(im,0,imy)
    gradientMagnitude = sqrt(imx**2 + imy**2)
    figure()
    gray()
    imshow(gradientMagnitude)
    show()

im = array(Image.open('square.jpg').convert('L'))

simpleOutline(im)