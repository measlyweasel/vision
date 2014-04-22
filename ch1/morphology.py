from scipy.ndimage import measurements, morphology
from numpy import *
from PIL import Image

# load image and threshold to make sure it is binary
im = array(Image.open('../data/houses.png').convert('L'))
im = 1*(im<128)

labels,nbr_objects = measurements.label(im)

print ("Number of objects:", nbr_objects)

#morphology
im_open = morphology.binary_opening(im, ones((9,5)),iterations=2)

labels_open, nbr_objects_open = measurements.label(im_open)

print ("Number of objects OPEN:", nbr_objects_open)