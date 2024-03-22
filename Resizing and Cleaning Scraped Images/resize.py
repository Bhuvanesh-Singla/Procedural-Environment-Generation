import torch
import torchvision.transforms.functional as fn
from PIL import Image
import matplotlib.pyplot as plt
import torchvision.transforms as T
import os

new_size=(256,256)
folder_path="C:\Imgs - Copy"

print("Resizing")
for filename in os.listdir(folder_path):
    if filename.endswith(".png"):
        image_path = os.path.join(folder_path, filename)
        img = Image.open(image_path)
        resized_img = img.resize(new_size)
        
        resized_img.save(image_path)
print("Resizing Done")
