from ultralytics import YOLO

# Load the YOLO model
model = YOLO('yolov8m.pt')

# Define a class mapping dictionary
class_mapping = {
    0: 'Michael Jackson', # The key is the class id, you may need to adjust according to your model
    # Add more mappings as needed
}

# Perform object detection on the image
path=r"C:\Users\my pc\OneDrive\Desktop\download.jpeg"
results = model(source=path)

# Replace class names with custom labels in the results
for result in results:
    for cls_id, custom_label in class_mapping.items():
        if cls_id in result.names: # check if the class id is in the results
            result.names[cls_id] = custom_label # replace the class name with the custom label

# Perform object detection on the image
results = model(source=path,save=True, conf=0.7)