import os
import cv2
import numpy as np
import random

def augment_image(image, applied_combinations):
    numtransforms = random.randint(2, 3)
    
    transformation_combination = tuple(random.sample(["horizontal_flip", "vertical_flip", "rotate_90", "rotate_180", "rotate_270", "contrast"], numtransforms))
    
    while transformation_combination in applied_combinations:
        transformation_combination = tuple(random.sample(["horizontal_flip", "vertical_flip", "rotate_90", "rotate_180", "rotate_270", "contrast"], numtransforms))

    applied_combinations.add(transformation_combination)

    for choice in transformation_combination:
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
        elif choice == "contrast":
            gamma = random.uniform(0.5, 2.0)
            image = (np.power(image.astype(np.float32) / 65535.0, gamma) * 65535).astype(np.uint16)

    return image

def augment_images_in_folder(input_folder, output_folder, num_augmentations):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.png'):
            image_path = os.path.join(input_folder, filename)
            original_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED).astype(np.uint16)

            
            applied_combinations = set()

            for _ in range(num_augmentations):
                augmented_image = augment_image(original_image, applied_combinations)
                output_path = os.path.join(output_folder, f"augmented_{filename.replace('.', f'-{_+1}.')}")
                cv2.imwrite(output_path, augmented_image)

input_folder = "C:\\Users\\Vedanth\\OneDrive\\Desktop\\original_raw\\"
output_folder = "C:\\Users\\Vedanth\\OneDrive\\Desktop\\augmentedimages\\"
number_augmentations = 3

augment_images_in_folder(input_folder, output_folder, number_augmentations)
