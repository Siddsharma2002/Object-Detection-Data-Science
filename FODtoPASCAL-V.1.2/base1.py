from ultralytics import YOLO

# Create and train YOLOv8 model from scratch (no pre-trained weights)
model = YOLO("yolov8l.yaml")  # Initializes the model architecture

# Define paths (use raw strings to avoid Windows path issues)
yaml_path = r"C:\Users\my pc\OneDrive\Desktop\New folder (5)\FODPascalVOCFormat-V.2.1\FODPascalVOCFormat-V.2.1\test1\config.yaml"

# Train the model on your custom dataset with 300x300 image size
model.train(data=yaml_path, epochs=100, batch=16, imgsz=300)  # Changed imgsz=300

# Optional: Save/export the trained model
model.export(format="pt")

print("✅ Training completed! The trained model is saved in 'runs/detect/train/weights/best.pt'.")
