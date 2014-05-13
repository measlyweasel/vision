from PIL import Image
from scipy.ndimage import filters
from numpy import *
from pylab import *
from scipy import misc
import itertools
import math

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
axis('off')
gray()
imshow(im)

sameAngle = vectorize(lambda angle, lowerBound, upperBound: 255 if angle >= lowerBound and angle <= upperBound else 0)

bins = [-pi, -pi * 3 / 4, -pi / 2, -pi / 4, 0, pi / 4, pi / 2, pi * 3 / 4, pi]

maskedAngles = (magnitude>averageMag)*angles

binnedAngles = digitize(maskedAngles.flatten(), bins)

def isSimilar(a, bin):
    return a == bin


isSimilarVectorized = vectorize(isSimilar)

#distance measured from different corners/edges
#depending on gradient angle (line direction)
def distanceBetweenPoints(point,origin):
    x=point[1] - origin[1]
    y=point[0] - origin[0]
    return math.sqrt(y**2 + x**2)

halfHeight=int(math.ceil(im.shape[0]/2))
halfWidth=int(math.ceil(im.shape[1]/2))
width=im.shape[1]
height=im.shape[0]

originPoints=[(0,halfWidth),(0,0),(halfHeight,0),(height,0),(0,halfWidth),(0,0),(halfHeight,0),(height,0)]

def minAndMaxPoint(pointList,bin):
    print("from origin ",originPoints[bin-1])
    min = distanceBetweenPoints(im.shape,(0,0))
    minPoint = (0,0)
    max = 0
    maxPoint = (0,0)
    for point in pointList:
        distance = distanceBetweenPoints(point,originPoints[bin-1])
        if distance > max:
            max = distance
            maxPoint = point
        if distance < min:
            min = distance
            minPoint = point
    return (minPoint,maxPoint)

#only need to go through half the bins since each straight line will have gradients
#pointing opposing directions at the line. Really only need to check half of the compass
#points because of this
for bin in range(1, int(ceil(len(bins)/2))):  #one based indexing of bins
    print("bin ", bin)
    similarAngledPoints = isSimilarVectorized(binnedAngles.reshape(im.shape), bin=bin)
    #imshow(similarAngledPoints)

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

    lengths = []
    for (y,x),value in ndenumerate(similarAngledPoints):
        connectedComponent = dfs(y,x)
        #picked a min length of 20 pixels as a cut off
        if len(connectedComponent)>19:
            (minPoint,maxPoint)=minAndMaxPoint(connectedComponent,bin)
            plot([minPoint[1],maxPoint[1]],[minPoint[0],maxPoint[0]])
            print(minPoint,maxPoint,connectedComponent)
show()



