import glob
import os
import numpy as np
from PIL import Image

imgList = glob.glob('C:\\Users\\Vedanth\\OneDrive\\Desktop\\Procedural Environment Dataset 2 After Cleaning\\*.png')
stdDevThresh = 2000  
blackThresh = 4000

for imgName in imgList:
    img = Image.open(imgName)
    pixels = img.getdata()

    # Check if image is un-varied
    stdDev = np.sqrt(np.var(pixels))

    if stdDev < stdDevThresh:  # not very varied picture
        print("deleting unvaried image: " + imgName)
        os.remove(imgName)
    else:
        # Check if image is dark
        numBlack = sum(1 for pixel in pixels if pixel < blackThresh)
        n = len(pixels)
        if (numBlack / float(n)) > 0.8:  # more than 80% of pixels are black
            print("deleting dark image: " + imgName)
            os.remove(imgName)

print('done with the dark and unvaried image cleanup!')
