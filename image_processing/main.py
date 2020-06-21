from PIL import Image
import os
import sys
import numpy as np
import cv2
import math
import urllib

# processes the large image, and the smaller ones
def get_processed_image(larger_image, images_8 = {}):

    if larger_image:


        # the larger image is the one that will be processed later
        # the images 8 is the group of images that will be passed in (or can simply be used through db and/or the file system)
        # images_8 is going to be all the names

        size_8 = (8, 8)
        larger_size = (256, 256)

        pictureRGB = {}
        faceAverages = []
        closestImages = []

        # Scripts to shrink down images to smaller size

        path = "./image_processing"

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
        for imagename in os.listdir(f'{path}/8images'):
            image = Image.open(f"{path}/8images/"+imagename)
            pictureRGB[imagename] = getAverageRGBN(image)

        for small_image_name, small_image in images_8.items():
            pictureRGB[small_image_name] = getAverageRGBN(small_image)
            

        im = np.array(larger_image)
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
            pix = larger_image.load()

            if ycounter == 255 and xcounter == 255:
                break
            if ycounter == endy and xcounter == 255:
                endy += 8
                endx = 7
                ycounter += 1
                xcounter = -1
                tempR = 0
                tempB = 0
                tempG = 0
            if ycounter == endy and xcounter == endx:
                ycounter -= 7
                endx += 8
                faceAverages.append([tempR/64, tempG/64, tempB/64])
                tempR = 0
                tempB = 0
                tempG = 0
            if xcounter == endx:
                xcounter -= 8
                ycounter += 1

            tempR += pix[xcounter, ycounter][0]
            tempG += pix[xcounter, ycounter][1]
            tempB += pix[xcounter, ycounter][2]

            xcounter += 1

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


        horizontalImages = []
        counter = 0

        new_im = Image.new('RGB', size = larger_size)

        y_offset = 0
            
        # going to loop through everything, building the images
        for i in range(31):
            
            images = []

            for x in closestImages[counter]:
                try:
                    images.append(Image.open(f'{path}/8images/{x}'))
                except:
                    images.append(images_8.get(x))


            widths, heights = zip(*(i.size for i in images))

            total_width = sum(widths)
            max_height = max(heights)

            new_im_x = Image.new('RGB', (total_width, max_height))

            x_offset = 0
            for im in images:
                new_im_x.paste(im, (x_offset, 0))
                x_offset += im.size[0]

            new_im.paste(new_im_x, (0, y_offset))
            y_offset += new_im_x.size[1]

            counter += 1

        print("Finished!")
        return new_im
    return None