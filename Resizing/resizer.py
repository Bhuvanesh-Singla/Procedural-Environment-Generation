import cv2
import numpy as np
import glob
import os

save_path = "/home/bhushi/Dataset"
img_path = "/home/bhushi/New_"
# os.makedirs(save_path)
lst=glob.glob(os.path.join(img_path, "*.png"))
for path in lst:
    print(path)
    # Load the 32-bit depth image (color)
    original_image = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    # Ensure the image is not None
    if original_image is not None:
        # Convert the color image to grayscale
        grayscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

        scaled_image = (grayscale_image / 255.0 * np.iinfo(np.uint16).max).astype(np.uint16)
        width, height = scaled_image.shape
        i = min(width, height)

        top_left = (0, 0)
        bottom_right = (i, i)
        # Crop the image
        cropped_image = scaled_image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        recrop=cv2.resize(cropped_image,(256,256),cv2.INTER_AREA)
        output_path = os.path.join(save_path, os.path.basename(path.replace('.png',"")+"_1.png"))
        cv2.imwrite(output_path, recrop)
        top_left = (height-i, width-i)
        bottom_right = (height,width )
        # Crop the image
        cropped_image = scaled_image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        recrop=cv2.resize(cropped_image,(256,256),cv2.INTER_AREA)
        output_path = os.path.join(save_path, os.path.basename(path.replace('.png',"")+"_2.png"))
        cv2.imwrite(output_path, recrop)
    else:
        print("Error: Unable to load the original image.")