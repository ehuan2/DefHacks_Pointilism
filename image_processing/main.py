from PIL import Image
import os
import sys
import numpy as np
import cv2
import math
import urllib

size_8 = (8, 8)
size_256 = (256, 256)

pictureRGB = {}
faceAverages = []
closestImages = []

# Scripts to shrink down images to smaller size

path1 = os.path.normpath(".")

for i in os.listdir(path1):
    if i.endswith(".png") and str(i) == "face.png":
        print("ah yes")
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
    w, h, d = im.shape
    # change shape
    im.shape = (w*h, d)
    # get average
    return tuple(np.average(im, axis=0))


# Average pixels in all images and save it to dict
for imagename in os.listdir('./8images'):
    image = Image.open("./8images/"+imagename)
    pictureRGB[imagename] = getAverageRGBN(image)

print("pic rgb")
print(pictureRGB)


image = Image.open("./finalImage/face.png")
im = np.array(image)
# get shape
w, h, d = im.shape

xcounter = 0
ycounter = 0

endx = 7
endy = 7

tempR = 0
tempG = 0
tempB = 0

tempCounter = 0

while True:
    pix = image.load()
    # print(image.size)
    # print(pix[xcounter,ycounter])

    print("XCounter = " + str(xcounter))
    print("YCounter = " + str(ycounter))
    print("endx = " + str(endx))
    print("endy = " + str(endy))

    if ycounter == 255 and xcounter == 255:
        #faceAverages.append([tempR/64, tempG/64, tempB/64])
        # print("appended")
        #tempR = 0
        #tempB = 0
        #tempG = 0
        break
    if ycounter == endy and xcounter == 255:
        endy += 8
        endx = 7
        ycounter += 1
        xcounter = -1
        print("face avg")
        tempR = 0
        tempB = 0
        tempG = 0
        # print(len(faceAverages))
    if ycounter == endy and xcounter == endx:
        ycounter -= 7
        endx += 8
        faceAverages.append([tempR/64, tempG/64, tempB/64])
        print("appended")
        tempR = 0
        tempB = 0
        tempG = 0
    if xcounter == endx:
        xcounter -= 8
        ycounter += 1

    tempR += pix[xcounter, ycounter][0]
    tempG += pix[xcounter, ycounter][1]
    tempB += pix[xcounter, ycounter][2]

   # print("special pix")
    #print(pix[125, 10])
    #print("R = " + str(tempR))
    #print("G = " + str(tempG))
    #print("B = " + str(tempB))

    xcounter += 1

print(faceAverages)


#print("len 1 = " + str(len(faceAverages[0])))
#print("len 2 = " + str(len(faceAverages[1])))


tempClosest = []
# Compare the 8x8 square colour average with the inputted image colours and determine which are closest.
for square in faceAverages:
    counter = 0
    diff = 100000
    closest = "none"
    for img in pictureRGB:
        colourDistance = math.sqrt((pictureRGB[img][0]-square[0])**2+(
            pictureRGB[img][1]-square[1])**2+(pictureRGB[img][2]-square[2])**2)
        if colourDistance < diff:
            diff = colourDistance
            closest = img
        counter += 1
        if counter == len(pictureRGB):
            tempClosest.append(closest)

        if len(tempClosest) == 31:
            closestImages.append(tempClosest)
            tempClosest = []

print(closestImages)


horizontalImages = []
counter = 0
for i in range(31):
    images = [Image.open(x) for x in closestImages[counter]]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    new_im.save('./horizontalImages/horiz' + str(counter) + '.jpg')
    horizontalImages.append('horiz' + str(counter) + '.jpg')

    counter += 1


print("horizontal images = ")
print(horizontalImages)


images = [Image.open("./horizontalImages/"+x) for x in horizontalImages]
widths, heights = zip(*(i.size for i in images))

total_width = max(widths)
max_height = sum(heights)

new_im = Image.new('RGB', (total_width, max_height))

y_offset = 0
for im in images:
    new_im.paste(im, (0, y_offset))
    y_offset += im.size[1]

new_im.save('./horizontalImages/final.jpg')
