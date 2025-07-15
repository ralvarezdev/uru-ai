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

# My device display
DISPLAY_WIDTH_PX = 1366
DISPLAY_HEIGHT_PX = 768
DISPLAY_DIAGONAL_INCH = 15.6

# PDF settings
PDF_FORMAT = "A4"
PDF_PT_UNIT = "pt"
PDF_MM_UNIT = "mm"
PDF_INCH_UNIT = "in"
PDF_PX_UNIT = "px"
PDF_MARGIN_MM = 20
PDF_TAB_WHITE_SPACE = 4

# A4 dimensions in mm
A4_WIDTH_MM = 210
A4_HEIGHT_MM = 297

# H1, H2 and H3 in px
H1_SIZE_PT = 12
H2_SIZE_PT = 12
H3_SIZE_PT = 12

# Text size in px
TEXT_SIZE_PT = 10

# Line height proportional to the text size
LINE_HEIGHT = 1.15