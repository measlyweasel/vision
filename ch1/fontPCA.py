from io import BytesIO
from PIL import Image
import ch1.pca as pca
from numpy import *
from pylab import *
from zipfile import ZipFile
import pickle

fontsZip = ZipFile('data/fontimages.zip','r')

# reverse engineered the zipfile's external attributes to get this bitwise operation
# the first 2 bytes in external_attr are unix file stat and the next 2 are windows
# stat.S_IFDIR is 0o040000 or 0b100000000000000 the 14th byte
# so scooting over the necessary 2 bytes gives bin(0o040000 << 16) = '0b1000000000000000000000000000000'
# so the 14th byte after an offset of 16 bytes equals (1 << 30) -jason
allImageNames = [x.filename for x in fontsZip.infolist() if not x.external_attr & (1 << 30)]

def imageFromInsideZip(fileName):
    data = fontsZip.open(fileName).read()
    fileLikeData = BytesIO(data)
    return Image.open(fileLikeData)

im = array(imageFromInsideZip(allImageNames[0])) # open the first image to get the size

width,height = im.shape[0:2]
imageCount=len(allImageNames)

#create a matrix to store all flattened images
imageMatrix = array([array(imageFromInsideZip(imageName)).flatten() for imageName in allImageNames], 'f')

#perform principle component analysis
V,S,imageMean = pca.pca(imageMatrix)

#show some images (mean and 7 first modes)
figure()
gray()
subplot(2,4,1)
#reshape conerts back from the flattened one dimensional representation
imshow(imageMean.reshape(width,height))
for i in range(7):
    subplot(2,4,i+2)
    imshow(V[i].reshape(width,height))

show()

# save this data to a pickle
with open ('font_pca_modes.pkl', 'wb') as f:
    pickle.dump(imageMean,f)
    pickle.dump(V,f)

#load from the pickle
# with open('font_pca_modes.pkl', 'rb') as f:
#   imageMean = pickle.load(f)
#   V = pickle.load(f)