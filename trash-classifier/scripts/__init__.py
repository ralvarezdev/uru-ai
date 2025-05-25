import os

# Current working directory
CWD = os.path.dirname(os.path.abspath(__file__))

# Dataset paths
DATASET = os.path.join(CWD, '../dataset')
DATASET_RESIZED = os.path.join(DATASET, 'resized')
DATASET_AUGMENTED = os.path.join(DATASET, 'augmented')
DATASET_ORGANIZED = os.path.join(DATASET, 'organized')
DATASET_ORGANIZED_TRAINING = os.path.join(DATASET_ORGANIZED, 'train')
DATASET_ORGANIZED_VALIDATIONS = os.path.join(DATASET_ORGANIZED, 'val')
DATASET_ORGANIZED_TESTING = os.path.join(DATASET_ORGANIZED, 'test')

# Model classes
CARDBOARD = 'cardboard'
PLASTIC = 'plastic'
PAPER = 'paper'
METAL = 'metal'
GLASS = 'glass'
TRASH = 'trash'
MODEL_CLASSES = (CARDBOARD, PLASTIC, PAPER, METAL, GLASS, TRASH)

# Augmentations
NUM_AUGMENTATIONS = 10

# Allowed image extensions
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg')