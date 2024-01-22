import os
import cv2
import imageio

folder_path = 'C:\\Users\\Vedanth\\OneDrive\\Desktop\\Procedural Environment Dataset After Resizing\\'
target_width, target_height = 256, 256

for filename in os.listdir(folder_path):
    image_path = os.path.join(folder_path, filename)
    
    
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED) 
    
    resized_image = cv2.resize(image, (target_width, target_height))
    
   
    imageio.imwrite(image_path, resized_image)

print("Resizing completed.")
