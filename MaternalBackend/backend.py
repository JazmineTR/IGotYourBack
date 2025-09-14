from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image

# Add YOLO import
try:
    from ultralytics import YOLO
    model = YOLO("yolov8n.pt")  # Will download automatically
    print("YOLO model loaded successfully")
except Exception as e:
    print(f"YOLO loading failed: {e}")
    model = None

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Objects to detect (relevant to maternal safety)
KEEP_CLASSES = [
    "chair", "couch", "bed", "dining table", "handbag", 
    "backpack", "suitcase", "desk"  # Use YOLO's class names
]

@app.get("/")
def root():
    return {"message": "FastAPI with Object Detection"}

@app.post("/predict_posture")
async def predict_posture(image: UploadFile = File(...)):
    try:
        print(f"Processing image: {image.filename}")
        
        # Read and convert image
        contents = await image.read()
        image_pil = Image.open(BytesIO(contents))
        frame = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
        
        print(f"Image converted, size: {frame.shape}")
        
        # Mock posture prediction (replace with your actual model)
        lumbar_angle = 35
        hip_angle = 20
        posture_status = "Safe Posture" if lumbar_angle > 30 else "Poor Posture - Risk"
        
        detections = []
        annotated_frame = frame.copy()
        
        if model is not None:
            # Run YOLO detection
            results = model.predict(frame, conf=0.3)
            
            for r in results:
                boxes = r.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get box coordinates and info
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        conf = float(box.conf[0])
                        cls = int(box.cls[0])
                        class_name = model.names[cls]
                        
                        print(f"Detected: {class_name} with confidence {conf}")
                        
                        # Only keep relevant objects
                        if class_name.lower() in [c.lower() for c in KEEP_CLASSES]:
                            # Choose color based on posture
                            color = (0, 255, 0) if "Safe" in posture_status else (0, 0, 255)  # BGR format
                            
                            # Draw bounding box
                            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 3)
                            
                            # Add label
                            label = f"{class_name} {conf:.2f}"
                            cv2.putText(annotated_frame, label, (x1, y1 - 10),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                            
                            # Store detection info
                            detection = {
                                'bbox': [x1, y1, x2 - x1, y2 - y1],
                                'confidence': conf,
                                'class': class_name,
                                'color': 'green' if "Safe" in posture_status else 'red'
                            }
                            detections.append(detection)
            
            print(f"Found {len(detections)} relevant objects")
        else:
            print("YOLO model not available - no detection performed")
        
        # Convert annotated frame back to base64
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        annotated_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return {
            "annotated_image": annotated_base64,
            "detections": detections,
            "posture_status": posture_status,
            "object_count": len(detections)
        }
        
    except Exception as e:
        print(f"Error processing image: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="10.203.67.159", port=5000, reload=True)