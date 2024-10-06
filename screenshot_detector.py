import os
import cv2
import json
from PIL import Image
from PIL.ExifTags import TAGS

def is_common_aspect_ratio(width, height):
    """Check if Image Aspect Ratio Matches Common Screen Ratios"""
    aspect_ratio = width / height
    common_ratios = [(16, 9), (4, 3), (21, 9)]

    for w, h in common_ratios:
        if abs(aspect_ratio - (w / h)) < 0.01: # Allowing for Slight Deviations
            return True
    return False

def has_screenshot_metadata(image_path):
    """Check if Image Metadata Contains Signs of a Screenshot"""
    image = Image.open(image_path)
    exif_data = image._getexif()
    if exif_data:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if "Screenshot" in str(value) or "Screen capture" in str(value):
                return True
    return False

def is_screenshot(image_path):
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    # Check if Aspect Ratio Matches Common Screen Aspect Ratios
    if is_common_aspect_ratio(width, height):
        return True
    
    # Check Screenshot Metadata
    if has_screenshot_metadata(image_path):
        return True
    
    return False

def process_images(input_folder="images", output_folder="output"):
    """
    Process all Images in the Input Folder and Determine if they are Screenshots
    Write the Results to a JSON File.
    """
    screenshot_data = {}

    # Create the Output Directory if it doesnt Exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through the Input Folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', 'jpeg')):
            image_path = os.path.join(input_folder, filename)

            try:
                # Analyze if the Image is a Screenshot
                is_ss = is_screenshot(image_path)
                screenshot_data[filename] = {"is_screenshot": is_ss}

                print(f"Processed {filename}: is_screenshot = {is_ss}")
            except Exception as e:
                print(f"Error Processing {filename}: {str(e)}")

    # Write the Results to the is_screenshot.json File Inside the Output Folder
    output_file = os.path.join(output_folder, "is_screenshot.json")
    with open(output_file, "w") as json_file:
        json.dump(screenshot_data, json_file, indent=4)

    print(f"Results Saved to {output_file}")

if __name__ == "__main__":
    process_images()