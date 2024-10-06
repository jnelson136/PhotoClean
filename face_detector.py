from mtcnn import MTCNN
import cv2
import os
import json

# Initialize MTCNN face detector
detector = MTCNN()

def load_image(image_path):
    """Loads an image from a given file path."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The image file {image_path} was not found.")
    return cv2.imread(image_path)

def detect_faces_mtcnn(image):
    """Detect faces using MTCNN."""
    result = detector.detect_faces(image)
    faces = [(r['box'][0], r['box'][1], r['box'][2], r['box'][3]) for r in result]
    return faces

def draw_faces(image, faces):
    """Draws rectangles around detected faces on the image."""
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    return image

def save_tagged_image(image, output_path):
    """Saves the image with faces highlighted to a file."""
    cv2.imwrite(output_path, image)

def process_image(image_path, output_path):
    """Processes a single image for face detection and saves the result."""
    image = load_image(image_path)
    faces = detect_faces_mtcnn(image)
    print(f"Detected {len(faces)} face(s) in {image_path}")
    
    tagged_image = draw_faces(image, faces)
    save_tagged_image(tagged_image, output_path)
    
    return len(faces)

def batch_process_images(input_directory, output_directory):
    """Batch processes all images in the input directory."""
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    face_data = {}

    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, f"tagged_{filename}")

            try:
                num_faces = process_image(image_path, output_path)
                face_data[filename] = {"faces_detected": num_faces}
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    with open(os.path.join(output_directory, "face_data.json"), "w") as json_file:
        json.dump(face_data, json_file, indent=4)
    print(f"Metadata saved to face_data.json")

if __name__ == "__main__":
    input_directory = "images"
    output_directory = "output"

    batch_process_images(input_directory, output_directory)
