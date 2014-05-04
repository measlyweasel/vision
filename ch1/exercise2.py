# Unsharp Masking
from PIL import Image
from scipy.ndimage import filters
from numpy import *
from pylab import *
from scipy import misc

imColor = misc.face()#array(Image.open('../data/empire.jpg'))
imGray = misc.lena() #array(Image.open('../data/empire.jpg').convert('L'))

sigma = 3
scale=0.25

def sharpen(image):
    out = zeros(image.shape)
    if (isinstance(image[0][0],list)) :
        for i in range(3):
            out[:,:,i] = image[:,:,i]-scale*filters.gaussian_filter(imColor[:, :, i], sigma)
    else:
        out = image-scale*filters.gaussian_filter(image,sigma)

    return uint8(out)

images = [imColor, sharpen(imColor),
          imGray, sharpen(imGray)]

gray()

for i in range(len(images)):
    subplot(2, len(images) / 2, i + 1)
    axis('off')
    imshow(images[i])

show()