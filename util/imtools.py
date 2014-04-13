import os
from numpy import *
from PIL import Image


def get_imlist(path):
    """
    Returns a list of filenames for
    all jpg images in a directory
    """
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]


def imresize(image, sz):
    """
    Resize an image array using PIL
    """
    pil_im = Image.fromarray(uint8(image))
    return array(pil_im.resize(sz))


def histeq(image, nBins=256):
    """
    Histogram equalization of a grayscale image
    """
    # get image histogram
    imhist, bins = histogram(image.flatten(), nBins, density=True)
    cdf = imhist.cumsum()  # cumulative distribution function
    cdf = 255 * cdf / cdf[-1]  #normalize

    #linear interpolation of cdf to find new pixel values
    im2 = interp(image.flatten(), bins[:-1], cdf)

    #reshape is a cool trick to unflatten the array
    return im2.reshape(image.shape), cdf


def compute_average(imageList):
    """
    Compute the average of a list of images
    """

    #initialize the output array with zeros
    imageShape = imageList[0].size
    averageim = zeros(imageShape,'f')

    imageCount = 0
    for image in imageList:
        try:
            averageim+=array(Image.open(image))
            ++imageCount
        except:
            print(image + '...skipped')

    averageim /= imageCount

    #pixel values can't be floats
    return array(averageim,'uint8')