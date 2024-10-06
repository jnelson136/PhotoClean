import os
import json
from PIL import Image
import imagehash

def compute_hash(image_path):
    """Compute the Perceptual Hash of an Image"""

    try:
        image = Image.open(image_path)
        return str(imagehash.average_hash(image))
    except Exception as e:
        print(f"Error Computing Hash for {image_path}: {str(e)}")
        return None

def detect_duplicates(input_folder="images", output_folder="output"):
    """
    Detects Duplicate Images in the Input Folder Based on Perceptual Hashing
    Saves Results to JSON File.
    """

    hashes = {}
    duplicates = {}

    # Create the Output Directory if it doesnt Exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate Over Images in the Folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)

            # Compute Hash for the Image
            image_hash = compute_hash(image_path)

            if image_hash:
                if image_hash in hashes:
                    # Mark as Duplicate if Hash Matches
                    duplicates[filename] = hashes[image_hash]
                    print(f"Duplicate Found: {filename} is a Duplicate of {hashes[image_hash]}")
                else:
                    # Save the Hash and Corresponding File Name
                    hashes[image_hash] = filename

    output_file = os.path.join(output_folder, "duplicate_data.json")          
    with open(output_file, "w") as json_file:
        json.dump(duplicates, json_file, indent=4)
    print(f"Results Saved to {output_file}")

if __name__ == "__main__":
    detect_duplicates()