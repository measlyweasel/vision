from PIL import Image
from scipy.ndimage import filters
from numpy import *
from pylab import *
from scipy import misc


def gradient(image):
    imx = zeros(image.shape)
    imy = zeros(image.shape)

    filters.sobel(image, 1, imx)
    filters.sobel(image, 0, imy)

    angles = arctan2(imy, imx)
    return (sqrt(imx ** 2 + imy ** 2), angles)


im = misc.ascent()

(magnitude, angles) = gradient(im)

figure()
gray()
imshow(im)

# for y in range(len(im)):
# for x in range(len(im[y])):
# if not visited[y][x] and abs(magnitude[y][x] - averageMag) > threshold:
# # follow the line, should be perpindicular to gradient angle
# angle = angles[y][x]
# nextPixelsAlongLine = radiansToRelativePixels(angle)
# print(angle, nextPixelsAlongLine)
#             plot(x, y, 'r*')
#         visited[y][x] = 1


sameAngle = vectorize(lambda angle, lowerBound, upperBound: 255 if angle >= lowerBound and angle <= upperBound else 0)

bins = [-pi, -pi * 3 / 4, -pi / 2, -pi / 4, 0, pi / 4, pi / 2, pi * 3 / 4, pi]

binnedAngles = digitize(angles.flatten(), bins)


def isSimilar(a, bin):
    binMinusOne = bin - 1 if bin - 1 else len(bins) - 1
    binPlusOne = bin + 1 if bin+1<len(bins) else 1
    return a == bin or a == binMinusOne or a == binPlusOne


isSimilarVectorized = vectorize(isSimilar)

for bin in range(1, len(bins)):  #one based indexing of bins
    print(bin)
    similarAngledPoints = isSimilarVectorized(binnedAngles.reshape(im.shape), bin=bin)
    print(similarAngledPoints)

    # for angle in unique(angles):
    #show()