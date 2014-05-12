from PIL import Image
from scipy.ndimage import filters
from numpy import *
from pylab import *
from scipy import misc
import itertools

def gradient(image):
    imx = zeros(image.shape)
    imy = zeros(image.shape)

    filters.sobel(image, 1, imx)
    filters.sobel(image, 0, imy)

    angles = arctan2(imy, imx)
    return (sqrt(imx ** 2 + imy ** 2), angles)


im = misc.ascent()

(magnitude, angles) = gradient(im)

averageMag = average(magnitude)

figure()
gray()
imshow(im)
show()

sameAngle = vectorize(lambda angle, lowerBound, upperBound: 255 if angle >= lowerBound and angle <= upperBound else 0)

bins = [-pi, -pi * 3 / 4, -pi / 2, -pi / 4, 0, pi / 4, pi / 2, pi * 3 / 4, pi]

maskedAngles = (magnitude>averageMag)*angles

binnedAngles = digitize(maskedAngles.flatten(), bins)

def isSimilar(a, bin):
    # binMinusOne = bin - 1 if bin - 1 else len(bins) - 1
    # binPlusOne = bin + 1 if bin+1<len(bins) else 1
    # return a == bin or a == binMinusOne or a == binPlusOne
    return a == bin


isSimilarVectorized = vectorize(isSimilar)

#only need to go through half the bins since each straight line will have gradients
#pointing opposing directions at the line. Really only need to check half of the compass
#points because of this
for bin in [1]:#range(1, int(ceil(len(bins)/2))):  #one based indexing of bins
    print("bin ", bin)
    similarAngledPoints = isSimilarVectorized(binnedAngles.reshape(im.shape), bin=bin)

    subplot(2,4,bin)
    imshow(similarAngledPoints)

    #now to find the connected components

    compassDirections = list(itertools.product([1,0,-1],repeat=2))
    compassDirections.remove((0,0))

    visited = zeros(similarAngledPoints.shape,dtype=bool)

    #depth first search
    def dfs(yPoint,xPoint):
        if not similarAngledPoints[yPoint][xPoint] or visited[yPoint][xPoint]:
            return []
        connectedComponent=[]
        stack = []
        stack.append((yPoint,xPoint))
        while stack:
            pixel = stack.pop()
            y = pixel[0]
            x = pixel[1]
            if not visited[y][x]:
                visited[y][x] = True
                if similarAngledPoints[y][x]:
                    connectedComponent.append((y,x))
                    for direction in compassDirections:
                        nextY = y+direction[0]
                        nextX = x+direction[1]

                        if nextY<0 or nextX<0 or nextY>=similarAngledPoints.shape[0] or nextX>=similarAngledPoints.shape[1]:
                            continue

                        if similarAngledPoints[nextY][nextX] and not visited[nextY][nextX]:
                            stack.append((nextY,nextX))
        return connectedComponent

    for (y,x),value in ndenumerate(similarAngledPoints):
        connectedComponent = dfs(y,x)
        if connectedComponent:
            print(y,x,connectedComponent)


show()



