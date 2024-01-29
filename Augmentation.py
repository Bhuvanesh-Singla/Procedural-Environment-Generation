import os
import cv2
import numpy as np
import random

def augment_image(image):
    choice = random.choice(["horizontal_flip", "vertical_flip", "rotate_90", "rotate_180", "rotate_270","contrast"])
    if choice == "horizontal_flip":
        image = np.fliplr(image)
    elif choice == "vertical_flip":
        image = np.flipud(image)
    elif choice == "rotate_90":
        image = np.rot90(image)
    elif choice == "rotate_180":
        image = np.rot90(image, k=2)
    elif choice == "rotate_270":
        image = np.rot90(image, k=3)
    elif choice=="contrast":
        gamma = random.uniform(0.5, 2.0)
        # Scale pixel values using gamma correction while preserving 16-bit depth
        image = (np.power(image.astype(np.float32) / 65535.0, gamma) * 65535).astype(np.uint16)

    return image

def augment_images_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.png'):
            image_path = os.path.join(input_folder, filename)
            original_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED).astype(np.uint16)
            augmented_image = augment_image(original_image)
            output_path = os.path.join(output_folder, f"augmented_{filename}")
            cv2.imwrite(output_path, augmented_image)


input_folder = "C:\cp"
output_folder = "C:\cp"

augment_images_in_folder(input_folder, output_folder)
