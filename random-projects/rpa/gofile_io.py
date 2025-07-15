from constants import SALES_REPORT_PDF

import requests

def upload_to_gofile(file_path):
    """
    Upload a file to GoFile.io and return the download link.

    Args:
        file_path (str): The path to the file to be uploaded.

    Returns:
        str: The download link for the uploaded file.
    """
    with open(file_path, 'rb') as f:
        response = requests.post(
            'https://upload.gofile.io/uploadfile',
            files={'file': f}
        )
    return response.json()['data']['downloadPage']