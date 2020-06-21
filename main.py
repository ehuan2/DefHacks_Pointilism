from PIL import Image
import os
import numpy as np
import cv2

size_8 = (8,8)
size_256 = (256,256)

pictureRGB = {}

# Scripts to shrink down images to smaller size
'''
for i in os.listdir('.'):
    if i.endswith(".png"):
        image = Image.open(i)
        fn, fext = os.path.splitext(i)
        image.thumbnail(size_256)
        image.save("./finalImage/face.png")
'''
'''
for i in os.listdir('./images'):
    if i.endswith(".jpg"):
        image = Image.open("./images/"+i)
        fn, fext = os.path.splitext(i)
        image.thumbnail(size_8)
        image.save("./8images/{}.png".format(fn))
'''

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

for imagename in os.listdir('./8images'):
    average = [0,0,0]
    image = Image.open("./8images/"+imagename)
    pictureRGB[imagename] = getAverageRGBN(image)

print(pictureRGB)

    






