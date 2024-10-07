import os
import json
from PIL import Image
import imagehash

stored_hashes = {}

def compute_hash(image_path):
    """Compute the Perceptual Hash of an Image"""

    try:
        image = Image.open(image_path)
        return str(imagehash.phash(image))
    except Exception as e:
        print(f"Error Computing Hash for {image_path}: {str(e)}")
        return None

def detect_duplicates(input_folder="images", output_folder="output", threshold=10):
    """
    Detects Duplicate Images in the Input Folder Based on Perceptual Hashing
    Saves Results to JSON File.
    """

    hashes = {}
    duplicates = {}

    # Create Output Directory if it doesnt Exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Iterate Over Images in Folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)

            # Compute Hash for Image
            image_hash = compute_hash(image_path)

            if image_hash:
                # Check for Duplicates
                duplicate_found = False
                for stored_hash in hashes.keys():
                    distance = imagehash.hex_to_hash(image_hash) - imagehash.hex_to_hash(stored_hash)

                    # If Distance is within Threshold, Mark as Duplicate
                    if distance == 0:
                        duplicates[filename] = {
                            "identical_duplicate_of": hashes[stored_hash],
                            "distance": distance
                        }
                        
                        print(f"Identical Duplicate Found! {filename} is Identical to {hashes[stored_hash]}")
                        duplicate_found = True
                        break
                    elif 0 < distance <= threshold:
                        duplicates[filename] = {
                            "near_duplicate_of": hashes[stored_hash],
                            "hamming_distance": distance
                        }
                        print(f"Near-Duplicate Found: {filename} is a Near Duplicate of {hashes[stored_hash]} with Hamming Distance: {distance}")

                if not duplicate_found:
                    hashes[image_hash] = filename

    # Write Duplicate Data to duplicate_data.json
    output_file = os.path.join(output_folder, "duplicate_data.json")
    with open(output_file, "w") as json_file:
        json.dump(duplicates, json_file, indent=4)
    print(f"Results Saved to {output_file}")


if __name__ == "__main__":
    detect_duplicates()