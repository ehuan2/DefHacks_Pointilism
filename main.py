from PIL import Image
import os
import numpy as np
import cv2
import math

size_8 = (8,8)
size_256 = (256,256)

pictureRGB = {}
faceAverages = []

# Scripts to shrink down images to smaller size

for i in os.listdir('.'):
    if i.endswith(".png"):
        image = Image.open(i)
        fn, fext = os.path.splitext(i)
        new_image = image.resize(size_256)
        new_image.save("./finalImage/face.png")


for i in os.listdir('./images'):
    if i.endswith(".jpg"):
        image = Image.open("./images/"+i)
        fn, fext = os.path.splitext(i)
        new_image = image.resize(size_8)        
        new_image.save("./8images/{}.png".format(fn))


def getAverageRGBN(image):
  """
  Given PIL Image, return average value of color as (r, g, b)
  """
  # get image as numpy array
  im = np.array(image)
  # get shape
  w,h,d = im.shape
  # change shape
  im.shape = (w*h, d)
  # get average
  return tuple(np.average(im, axis=0))


# Average pixels in all images and save it to dict
for imagename in os.listdir('./8images'):
    image = Image.open("./8images/"+imagename)
    pictureRGB[imagename] = getAverageRGBN(image)

print(pictureRGB)





image = Image.open("./finalImage/face.png")
im = np.array(image)
# get shape
w,h,d = im.shape

xcounter = 0
ycounter = 0

endx = 7
endy = 7

tempR = 0
tempG = 0
tempB = 0

while True:
    pix = image.load()
    #print(image.size)
    #print(pix[xcounter,ycounter])

    print("XCounter = " + str(xcounter))
    print("YCounter = " + str(ycounter))
    print("endx = " + str(endx))
    print("endy = " + str(endy))

    if ycounter == 255 and xcounter == 255:
        break
    if ycounter == endy and xcounter == 255:
        endy +=8
        ycounter += 1
        xcounter = -1
    if ycounter == endy and xcounter == endx:
        ycounter = 0
        endx += 8
        faceAverages.append([tempR/64, tempG/64, tempB/64])
    if xcounter == endx:
        xcounter -=8
        ycounter += 1
    
    tempR += pix[xcounter, ycounter][0]
    tempG += pix[xcounter, ycounter][1]
    tempB += pix[xcounter, ycounter][2]
    xcounter+=1
 
print(faceAverages)
    






