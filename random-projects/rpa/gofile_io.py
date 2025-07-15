from constants import SALES_REPORT_PDF

import requests

def upload_to_gofile(file_path):
    """
    Upload a file to GoFile.io and return the download link.

    Args:
        file_path (str): The path to the file to be uploaded.

    Returns:
        list: A list containing the page link and direct download link.
    """
    with open(file_path, 'rb') as f:
        response = requests.post(
            'https://upload.gofile.io/uploadfile',
            files={'file': f}
        ).json()

    if response['status'] == 'ok':
        data = response['data']
        page_link = data['downloadPage']
        return [page_link, data['servers'][0], data['id'], data['name']]
    else:
        raise Exception(f"Upload failed: {response}")