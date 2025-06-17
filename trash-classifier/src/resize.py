import os
from time import time
import cv2

from .files import Files


def resize_image(input_path, output_dir, image_filename):
    """
    Resize images.
    """
    # Get current time
    start_time = time()

    # Read the image and convert it to RGB
    image = cv2.imread(input_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Resize the image
    image = cv2.resize(image, (Files.IMAGE_SIZE, Files.IMAGE_SIZE))

    # Convert the image back to BGR and save it
    output_path = os.path.join(output_dir, image_filename)
    cv2.imwrite(output_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

    # Log the image
    end_time = time()
    elapsed_time = end_time - start_time
    print(f"Resized image saved to {output_path} in {elapsed_time:.2f} seconds")


def resize_dataset():
    """
    Resize a dataset.
    """
    # Check if the dataset directories exist, if not it creates them
    for io_dir in [Files.DATASET_ORIGINAL, Files.DATASET_RESIZED]:
        os.makedirs(io_dir, exist_ok=True)

    for _, model_class in enumerate(Files.MODEL_CLASSES):
        # Get the input and output directories
        input_dir = os.path.join(Files.DATASET_ORIGINAL, model_class)
        output_dir = os.path.join(Files.DATASET_RESIZED, model_class)

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
            resize_image(input_image_path, output_dir, image_filename)

def main():
    """
    Main function to run the script.
    """
    # Resize the dataset
    resize_dataset()

if __name__ == '__main__':
    main()