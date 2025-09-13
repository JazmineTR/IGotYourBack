from ultralytics import YOLO
import cv2
from model.posture_model import predict_posture
model = YOLO("yolov8n-oiv7.pt")
keep_classes = ["Infant bed", "Chair", "Table", "Handbag", 
                "Backpack", "Couch", "Desk", "Suitcase",
                "Cabinetry", "Chest of drawers", "Bed"]
cap = cv2.VideoCapture(1)

def scan_objects():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        lumbar_angle, hip_angle = 35, 18
        posture_status = predict_posture(lumbar_angle, hip_angle)

        results = model.predict(frame, conf=0.2) 
        r = results[0]

        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]
            conf = float(box.conf[0])

            if label in keep_classes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                color = (0, 255, 0) if "Safe" in posture_status else (0, 0, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                text = f"{label} {conf:.2f} | {posture_status}"
                cv2.putText(frame, text,
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (0, 255, 0), 2)

        cv2.imshow("Maternal Wellness Demo", frame)

        if cv2.waitKey(1) & 0xFF in [27, ord('q')]:  # ESC or q to quit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_objects()