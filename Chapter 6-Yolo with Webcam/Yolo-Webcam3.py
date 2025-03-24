from ultralytics import YOLO
import cv2
import cvzone
import math
import time

#cap = cv2.VideoCapture(r"C:\Users\my pc\OneDrive\Desktop\test-video-1.mp4")
cap = cv2.VideoCapture(r"C:\Users\my pc\OneDrive\Desktop\test-3.mp4")
#"C:\Users\my pc\OneDrive\Desktop\test-2.mp4"
model = YOLO("../Yolo-Weights/yolov8l.pt")

# Get class names directly from the model
classNames = model.names  # Dictionary {0: 'person', 1: 'bicycle', ...}

prev_frame_time = 0
new_frame_time = 0

while True:
    success, img = cap.read()
    if not success:
        break

    results = model(img, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1

            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class ID
            cls_id = int(box.cls[0])

            # Get class name, replacing "person" with "debris"
            label = "debris" if classNames[cls_id] == "sports ball" else classNames[cls_id]

            # Draw bounding box
            cvzone.cornerRect(img, (x1, y1, w, h), l=10)

            # Display modified class name
            cvzone.putTextRect(img, f'{label} {conf}%', (max(0, x1), max(35, y1)), scale=1, thickness=1, offset=5)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
