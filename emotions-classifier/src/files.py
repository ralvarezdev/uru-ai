import os

from .lib.files import Files as F

class Files(F):
    """
    Files utility class.
    """
    # Current working directory
    CWD = os.path.dirname(os.path.abspath(__file__))

    # Dataset paths
    DATASET = os.path.join(CWD, '../dataset')
    DATASET_ORIGINAL = os.path.join(DATASET, 'original')
    DATASET_AUGMENTED = os.path.join(DATASET, 'augmented')
    DATASET_ORGANIZED = os.path.join(DATASET, 'organized')
    DATASET_ORGANIZED_TRAINING = os.path.join(DATASET_ORGANIZED, 'train')
    DATASET_ORGANIZED_VALIDATIONS = os.path.join(DATASET_ORGANIZED, 'val')
    DATASET_ORGANIZED_TESTING = os.path.join(DATASET_ORGANIZED, 'test')

    # Model paths
    RUNS = os.path.join(CWD, '../runs')
    RUNS_WEIGHTS = os.path.join(RUNS, 'weights')
    RUNS_WEIGHTS_BEST_PT = os.path.join(RUNS_WEIGHTS, 'best.pt')

    # Model classes
    ANGRY = 'angry'
    FEAR = 'fear'
    HAPPY = 'happy'
    NEUTRAL = 'neutral'
    SAD = 'sad'
    SURPRISE = 'surprise'
    MODEL_CLASSES = (ANGRY, FEAR, HAPPY, NEUTRAL, SAD, SURPRISE)

    # Augmentations
    NUM_AUGMENTATIONS = 3

    # Allowed image extensions
    IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg')