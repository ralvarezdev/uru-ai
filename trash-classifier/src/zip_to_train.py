import os
from shutil import rmtree
import zipfile

from typing_extensions import LiteralString

from .lib.files.zip import Zip
from .files import Files

def zip_to_train(input_dir: LiteralString, input_yolo_dataset_organized_dir: LiteralString,
                 output_zip_dir: LiteralString) -> None:
    """
    Define the function to zip the required files for model training.

    Args:
        input_dir (str): The base input directory where the YOLO files are located.
        input_yolo_dataset_organized_dir (str): The directory containing the organized dataset files.
        output_zip_dir (str): The directory where the output zip file will be saved.

    Returns:
        None
    """
    # Define the output zip filename
    output_zip_filename = 'organized.zip'
    output_zip_path = os.path.join(output_zip_dir, output_zip_filename)

    # Check if the folder exists, if not create it
    Files.ensure_directory_exists(output_zip_dir)

    with (zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf):
        # Zip the YOLO dataset organized files
        Zip.zip_nested_folder(zipf, input_dir, input_yolo_dataset_organized_dir)
        print('Zip the YOLO dataset organized files')

    # Remove the original dataset organized folder
    rmtree(input_yolo_dataset_organized_dir)


def main() -> None:
    """
    Main function to run the script.
    """
    # Zip files
    zip_to_train(Files.CWD, Files.DATASET_ORGANIZED, Files.DATASET)


if __name__ == '__main__':
    main()
