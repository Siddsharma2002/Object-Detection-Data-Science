from ultralytics import YOLO
import cv2
import cvzone
import math

#cap = cv2.VideoCapture(r"C:\Users\my pc\OneDrive\Desktop\test-video-1.mp4")
cap = cv2.VideoCapture(r"C:\Users\my pc\OneDrive\Desktop\test-3.mp4")
model = YOLO("../Yolo-Weights/yolov8l.pt")

while True:
    success, img = cap.read()
    if not success:
        break  # Exit loop if video ends

    results = model(img, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1

            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100

            # Assign label based on confidence
            label = "Debris" if conf <= 40 else "Unknown"

            # Draw bounding box
            cvzone.cornerRect(img, (x1, y1, w, h), l=10)

            # Display modified class name
            cvzone.putTextRect(img, f'{label} {conf}%', (max(0, x1), max(35, y1)), scale=1, thickness=1, offset=5)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
