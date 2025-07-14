import os

# Sales sheet file path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
SALES_XLSX = os.path.join(DATA_DIR, 'sales.xlsx')

# Fonts path
FONTS_DIR = os.path.join(ROOT_DIR, 'fonts')
FIRA_CODE_REGULAR = os.path.join(FONTS_DIR, 'Fira_Code', 'static',
                         'FiraCode-Regular.ttf')
FIRA_CODE_BOLD = os.path.join(FONTS_DIR, 'Fira_Code', 'static',
                            'FiraCode-Bold.ttf')