import cv2
import os
import json
import numpy as np

def detect_low_light(image, brightness_threshold=40):
    """
    Detects if an Image is Underexposed (Low-Light) by Calculating Average Brightness
    """
    # Convert Image to Grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate Average Brightness
    avg_brightness = np.mean(gray_image)
    
    return avg_brightness < brightness_threshold

def detect_overexposure(image, overexposure_threshold=250, overexposure_ratio=0.3):
    """
    Detects if an Image is Overexposed by Checking the Ratio of Overexposed Pixels.
    """

    # Convert Image to Grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Count the Number of Overexposed Pixels
    num_overexposed_pixels = np.sum(gray_image > overexposure_threshold)
    total_pixels = gray_image.size

    # Calculate Ratio of Overexposed Pixels
    overexposed_percentage = num_overexposed_pixels / total_pixels

    return overexposed_percentage > overexposure_ratio

def save_quality_data(image_name, quality_data, output_folder="output"):
    """
    Saves Photo Quality Detection Results to a JSON File
    """
    # Convert numpy bools to Python bools
    for key, value in quality_data.items():
        if isinstance(value, np.bool_):
            quality_data[key] = bool(value)


    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Path to JSON File
    json_file_path = os.path.join(output_folder, "photo_quality_data.json")

    # Load Existing Data if the File Exists
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
    else:
        data = {}
    
    data[image_name] = quality_data

    # Save Updated Data to JSON File
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def process_images(input_folder="images", output_folder="output"):
    """
    Process All Images in Input Folder for Photo Quality
    """

    supported_formats = ('.jpg', '.jpeg', '.png')

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(supported_formats):
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)

            if image is not None:
                # Detect Low-Light and Overexposure
                is_low_light = detect_low_light(image)
                is_overexposed = detect_overexposure(image)

                quality_data = {
                    "is_low_light": is_low_light,
                    "is_overexposed": is_overexposed
                }

                # Save the Quality Data
                save_quality_data(filename, quality_data, output_folder)

                # Output Results to Console
                print(f"Processed {filename}: Low-Light = {is_low_light}, Overexposed = {is_overexposed}")
            else:
                print(f"Error Loading: {filename}")
if __name__ == "__main__":
    process_images()
