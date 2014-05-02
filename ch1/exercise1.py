from PIL import Image
from numpy import *
from scipy.ndimage import filters
from pylab import *

#blurring the same image with several different values of sigma
im = array(Image.open('../data/empire.jpg').convert('L'))
images = [im]

images.append(filters.gaussian_filter(im,10))
images.append(filters.gaussian_filter(im,20))
images.append(filters.gaussian_filter(im,20))
images.append(filters.gaussian_filter(im,30))


figure()
gray()
for i in range(len(images)):
    subplot(2,5,i+1)
    imshow(images[i])
    subplot(2,5,i+6)
    hist(images[i].flatten(),128)
show()

for i in range(len(images)):
    subplot(2,5,i+1)
    imshow(images[i])
    subplot(2,5,i+6)
    contour(images[i], origin='image')
show()


