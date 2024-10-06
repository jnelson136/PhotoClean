from flask import Flask, request, jsonify
import cv2
import numpy as np
from face_detector import detect_faces_mtcnn, batch_process_images # Import Detection Logic
from blur_detector import detect_blur, save_blur_data
from screenshot_detector import is_screenshot

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No Image Uploaded"}), 400
    
    file = request.files['image']
    npimg = np.fromfile(file, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Get the Filename for Saving Results
    filename = file.filename

    # Run Face Detection
    faces = detect_faces_mtcnn(image)

    # Run Blur Detection
    blur_score, is_blurry = detect_blur(image)
    # Save Blur Detection Results
    save_blur_data(filename, blur_score, is_blurry)

    # Screenshot Detection
    screenshot = is_screenshot(file.filename)

    # Decide if Photo is Worth Keeping
    worth_keeping = len(faces) > 0 and not is_blurry and not screenshot

    # Return Number of Faces Detected
    return jsonify({
        "faces_detected": len(faces),
        "blur_score": blur_score,
        "is_blurry": is_blurry,
        "screenshot": screenshot,
        "worth_keeping": worth_keeping
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)