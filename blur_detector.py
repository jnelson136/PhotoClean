import cv2
import os
import json


def detect_blur(image):
    """
    Detects if an Image is Blurry by Calculating the Variance of the Laplacian.
    Returns the Blur Score (variance) and a Boolean Indicating if the Image is Blurry
    """

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray_image, cv2.CV_64F).var()

    blur_threshold = 100.0 # Adjust Based on Testing
    is_blurry = laplacian_var < blur_threshold

    return laplacian_var, is_blurry

def save_blur_data(image_name, blur_score, is_blurry, output_folder="output"):
    """Saves Blur Detection Results (Blur Score and if its Blurry) to a JSON File"""

    # Convert NumPy Bool to Regular Python Bool
    is_blurry = bool(is_blurry)

    # Create the output folder if it doesnt exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    
    # Path to JSON File
    json_file_path = os.path.join(output_folder, "blur_data.json")

    # Load Existing Data if the File Exists
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            blur_data = json.load(json_file)

    else:
        blur_data = {}
    
    # Add New Data for this Image
    blur_data[image_name] = {
        "blur_score": blur_score,
        "is_blurry": is_blurry
    }

    # Write the Updated Data back to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(blur_data, json_file, indent=4)


def process_image(input_folder="images", output_folder="output"):
    """Processes all Images in the Input Folder for Blur Detection and Saves Results"""
    
    supported_formats = ('.jpg', '.jpeg', '.png')
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(supported_formats):
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)

            if image is not None:
                blur_score, is_blurry = detect_blur(image)
                save_blur_data(filename, blur_score, is_blurry, output_folder)
                print(f"Processed {filename}: Blur Score = {blur_score}, Blurry = {is_blurry}")
            else:
                print(f"Error Loading {filename}")

if __name__ == "__main__":
    process_image()