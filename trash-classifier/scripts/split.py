import argparse
import random
import os
import shutil
from typing import LiteralString

from scripts import MODEL_CLASSES, DATASET_AUGMENTED, DATASET_ORGANIZED, DATASET_ORGANIZED_TRAINING, \
    DATASET_ORGANIZED_VALIDATIONS, DATASET_ORGANIZED_TESTING


def split_dataset(train_ratio=0.7,
                  val_ratio=0.2):
    """
    Split the dataset into training, validation, and testing sets.
    """
    for _, model_class in enumerate(MODEL_CLASSES):
        # Get the input and output directories
        input_dir = os.path.join(DATASET_AUGMENTED, model_class)
        output_training_dir = os.path.join(DATASET_ORGANIZED_TRAINING, model_class)
        output_validations_dir = os.path.join(DATASET_ORGANIZED_VALIDATIONS, model_class)
        output_testing_dir = os.path.join(DATASET_ORGANIZED_TESTING, model_class)

        for io_dir in [input_dir, output_training_dir, output_validations_dir, output_testing_dir]:
            # Ensure the input and output directories exist
            os.makedirs(io_dir, exist_ok=True)

        # Get the list of files
        image_filenames = os.listdir(input_dir)
        if len(image_filenames) == 0:
            print(f"Warning: No images found in {input_dir}")
            return

        random.shuffle(image_filenames)

        # Split the dataset
        train_split = int(len(image_filenames) * train_ratio)
        val_split = int(len(image_filenames) * val_ratio)

        # Copy the files to the output directories
        for i, image_filename in enumerate(image_filenames):
            # Get the image paths
            input_image_path = os.path.join(input_dir, image_filename)

            if i < train_split:
                shutil.copy(input_image_path, output_training_dir)
            elif i < train_split + val_split:
                shutil.copy(input_image_path, output_validations_dir)
            else:
                shutil.copy(input_image_path, output_testing_dir)

            # Log
            print(f'Copied {image_filename} to the respective directories')

    # Remove the augmented dataset
    shutil.rmtree(DATASET_AUGMENTED)

def main() -> None:
    """
    Main function to run the script.
    """

    # Split the images
    split_dataset()

if __name__ == '__main__':
    main()