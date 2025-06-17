import os
from shutil import rmtree
from time import time
import cv2
import albumentations as A

from .files import Files

def augment_image(input_path, output_dir, image_filename, num_augmentations):
    """
    Augment images.
    """
    # Get current time
    start_time = time()

    # Read the image and convert it to RGB
    image = cv2.imread(input_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Define the pipeline
    transform = A.Compose([
        # Apply with a 50% probability a random brightness and contrast adjustment
        A.RandomBrightnessContrast(p=0.5),

        # Apply with a 50% probability a horizontal flip
        A.HorizontalFlip(p=0.5),

        # Apply with a 50% probability a random shift, scale, and rotation
        A.ShiftScaleRotate(shift_limit=0.2, scale_limit=0.2, rotate_limit=25, p=0.5),

        # Apply with a 30% probability a random RGB shift
        # A.RGBShift(r_shift_limit=25, g_shift_limit=25, b_shift_limit=25, p=0.3),
        # Currently, this is being on hold because it may trigger incorrect labels due to the color shift

        # Apply with a 30% probability a random crop
        A.RandomCrop(width=int(image.shape[1] * 0.9), height=int(image.shape[0] * 0.9), p=0.3),  # Optional random crop
    ])

    # Apply the pipeline to the image and annotations
    for i in range(num_augmentations):
        # Apply the transformation
        transformed = transform(image=image)
        transformed_image = transformed['image']

        # Convert the image back to BGR and save it
        output_path = os.path.join(output_dir, image_filename.replace('.jpg', f'_{i}.jpg'))
        cv2.imwrite(output_path, cv2.cvtColor(transformed_image, cv2.COLOR_RGB2BGR))

        # Log the image
        end_time = time()
        elapsed_time = end_time - start_time
        print(f"Augmented image saved to {output_path} in {elapsed_time:.2f} seconds")


def augment_dataset(num_augmentations = Files.NUM_AUGMENTATIONS):
    """
    Augment a dataset.
    """
    # Check if the dataset directories exist, if not it creates them
    for io_dir in [Files.DATASET_RESIZED, Files.DATASET_AUGMENTED]:
        os.makedirs(io_dir, exist_ok=True)

    for _, model_class in enumerate(Files.MODEL_CLASSES):
        # Get the input and output directories
        input_dir = os.path.join(Files.DATASET_RESIZED, model_class)
        output_dir = os.path.join(Files.DATASET_AUGMENTED, model_class)

        # Ensure the input and output directories exist
        for io_dir in [input_dir, output_dir]:
            os.makedirs(io_dir, exist_ok=True)

        # Get the image files
        image_filenames = [f for f in os.listdir(input_dir) if
                           f.lower().endswith(Files.IMAGE_EXTENSIONS)]

        # Augment each image
        for image_filename in image_filenames:
            print(f"Augmenting {image_filename}")

            # Get the image paths
            input_image_path = os.path.join(input_dir, image_filename)
            augment_image(input_image_path, output_dir, image_filename, num_augmentations)

    # Remove the resized dataset directory
    rmtree(Files.DATASET_RESIZED)

def main():
    """
    Main function to run the script.
    """
    # Augment the dataset
    augment_dataset()

if __name__ == '__main__':
    main()