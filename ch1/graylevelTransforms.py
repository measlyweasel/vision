from PIL import Image
from pylab import *
from numpy import *

#original image
image = array(Image.open('../data/empire.jpg').convert('L'))
gray()

#invert image
image2 = 255-image

#clamp between 100 and 200
image3 = (100.0/255)*image+100

#square and normalize
image4 = 255.0 * (image/255)**2

imshow(image)

figure()
imshow(image2)

figure()
imshow(image3)

figure()
imshow(image4)
show()
