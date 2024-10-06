import os
import json
from PIL import Image
import imagehash

def compute_hash(image_path):
    """Compute the Perceptual Hash of an Image"""