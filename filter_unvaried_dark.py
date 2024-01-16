############################################################
###### Run this script within the source image folder ######
############################################################
import PIL
import glob
import os
import shutil
import numpy as np
from PIL import Image


# next, delete dark and/or unvaried images
imgList = glob.glob('*.png')
stdDevThresh = 2000             # good = 8000-13000, dark = 200-1800
blackThresh = 4000
src = '.'
removable  = r"C:\Users\singl\Desktop\Bhuvanesh\NITK\Procedural Environment Generation\Dataset\skydark\removable"
for imgName in imgList:
    img_path = os.path.join(src,imgName)
    try:
        img = Image.open(imgName)
    except PIL.UnidentifiedImageError as e:
        print('bad image')
        dest = os.path.join(removable, imgName)
        shutil.move(img_path, dest)
        continue
    pixels = img.getdata()      # get the pixels as a vector

    ## check if image is un-varied
    stdDev = np.sqrt(np.var(pixels)) # get variance

    if stdDev < stdDevThresh:      # not very varied picture
        print(stdDev)
        print("deleting unvaried image:" + imgName)
        # os.remove(imgName)
        dest = os.path.join(removable, imgName)
        shutil.move(img_path, dest)

    else: # it's not un-varied, but it might still be too dark
        ## check if image is dark:
        numBlack = 0
        for pixel in pixels:
            if pixel < blackThresh:
                numBlack += 1
        # get percentage of black pixels:
        n = len(pixels)
        if (numBlack / float(n)) > 0.8:       # more than 50% of pixels are black
            print("deleting dark image:" + imgName)
            # os.remove(imgName)
            dest = os.path.join(removable, imgName)
            shutil.move(img_path, dest)
        else:
            print('passed')

print('done unvaried!')

