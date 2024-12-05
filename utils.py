import os 
import config
import cv2
import supervision as sv
from ultralytics import YOLO
import tempfile

# Khởi tạo mô hình YOLO
model = YOLO('model/best.pt') 

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

# Image processing function
def process_image(input_image_path: str, output_image_path: str):
    # Read the image
    image = cv2.imread(input_image_path)
    
    if image is None:
        print("Error: Unable to read the image!")
        return
    
    # Resize the image
    resized = cv2.resize(image, (640, 640))

    # Perform detection
    results = model(resized)
    detections = sv.Detections.from_ultralytics(results[0])
    print(detections)

    # Annotate the image
    box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()
    
    annotated = box_annotator.annotate(scene=resized, detections=detections)
    annotated = label_annotator.annotate(scene=annotated, detections=detections)

    # Save the annotated image
    cv2.imwrite(output_image_path, annotated)
    print(f"Processed and saved: {output_image_path}")