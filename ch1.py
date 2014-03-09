from PIL import Image
from pylab import *

image = array(Image.open('data/empire.jpg').convert('L'))
gray()

image2 = 255-image

image3 = (100.0/255)*image+100

image4 = 255.0 * (image/255)**2


imshow(image)

figure()
imshow(image2)

figure()
imshow(image3)

figure()
imshow(image4)
show()
