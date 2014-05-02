from PIL import Image
from numpy import *
from scipy.ndimage import filters
from pylab import *


#blurring a gray scale
im = array(Image.open('../data/empire.jpg').convert('L'))
sigma = 5
im2 = filters.gaussian_filter(im,sigma)

figure()
gray()
subplot(1,2,1)
imshow(im)

subplot(1,2,2)
imshow(im2)

show()

#blurring a color image
im = array(Image.open('../data/empire.jpg'))
im2 = zeros(im.shape)
for i in range(3):
    #blur each color channel individually
    im2[:,:,i] = filters.gaussian_filter(im[:,:,i],5)
im2 = uint8(im2)

figure()
subplot(1,2,1)
imshow(im)

subplot(1,2,2)
imshow(im2)
show()


#blurring the same image with several different values of sigma
im = array(Image.open('../data/empire.jpg').convert('L'))
images = [im]

images.append(filters.gaussian_filter(im,2))
images.append(filters.gaussian_filter(im,5))
images.append(filters.gaussian_filter(im,10))
images.append(filters.gaussian_filter(im,15))


figure()
gray()
for i in range(len(images)):
    subplot(1,5,i+1)
    imshow(images[i])
show()

