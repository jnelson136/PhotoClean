from PIL import Image
import os
import json

def is_image_corrupted(image_path):
    """
    Detect if an Image is Corrupted or Partially Loaded
    """

    try:
        # Open Image using PIL
        img = Image.open(image_path)

        # Verify Image File (Checks if the Image File is Complete and not Corrupted)
        img.verify()

        # Try Loading the Image Fully (to Catch Truncated Images)
        img = Image.open(image_path)
        img.load()

        return False # If no Exception is Raised, the Image is not Corrupted
    
    except (IOError, SyntaxError) as e:
        # If any Error is Raised, the Image is Corrupted
        print(f"Image at {image_path} is Corrupted: {e}")

        return True
    
def save_corruption_data(image_name, is_corrupted, output_folder="output"):
    """
    Saves Image Corruption Detection Results to JSON File
    """

    # Create the Output Folder if it doesn't Exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Path to JSON File
    json_file_path = os.path.join(output_folder, "corruption_data.json")

    # Load Existing Data if the File Exists
    try:
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
        else:
            data = {}
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error Reading JSON File: {e}. Recreating the File")
        data = {}
    
    data[image_name] = {
        "is_corrupted": is_corrupted
    }

    # Save Updated Data to the JSON File
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def process_images(input_folder="images", output_folder="output"):
    """
    Process all Images in the Input Folder to Detect Corruptedd Images.
    """

    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(supported_formats):
            image_path = os.path.join(input_folder, filename)

            # Detect if Image is Corrupted
            is_corrupted = is_image_corrupted(image_path)

            # Save Corruption Data
            save_corruption_data(filename, is_corrupted, output_folder)

            # Output Result to Console
            print(f"Processed {filename}: Corrupted = {is_corrupted}")

if __name__ == "__main__":
    process_images()