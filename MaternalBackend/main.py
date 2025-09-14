# Flask server that integrates with your existing AR code
from ultralytics import YOLO
import cv2
from model.posture_model import predict_posture
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import base64
import threading
from io import BytesIO
from PIL import Image

# Initialize your existing model and settings
model = YOLO("yolov8n-oiv7.pt")
keep_classes = ["Infant bed", "Chair", "Table", "Handbag", 
                "Backpack", "Couch", "Desk", "Suitcase",
                "Cabinetry", "Chest of drawers", "Bed"]

app = Flask(__name__)
CORS(app)  # Enable CORS for Expo app

# Your original scan_objects function, modified to work with frames from Expo
def process_frame_with_ar(frame, lumbar_angle=35, hip_angle=18):
    """
    Process a single frame with your AR logic
    Returns processed frame and detection data
    """
    # Your original posture prediction
    posture_status = predict_posture(lumbar_angle, hip_angle)

    # Your original YOLO prediction
    results = model.predict(frame, conf=0.2) 
    r = results[0]
    
    detections = []
    processed_frame = frame.copy()

    # Your original detection loop
    for box in r.boxes:
        cls = int(box.cls[0])
        label = model.names[cls]
        conf = float(box.conf[0])

        if label in keep_classes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # Your original color logic
            color = (0, 255, 0) if "Safe" in posture_status else (0, 0, 255)
            
            # Draw rectangle and text (your original code)
            cv2.rectangle(processed_frame, (x1, y1), (x2, y2), color, 2)
            text = f"{label} {conf:.2f} | {posture_status}"
            cv2.putText(processed_frame, text,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (0, 255, 0), 2)
            
            # Create detection object for Expo app
            detection = {
                'bbox': [x1, y1, x2 - x1, y2 - y1],  # [x, y, width, height]
                'confidence': conf,
                'class': label,
                'class_id': cls,
                'posture_status': posture_status,
                'color': 'green' if "Safe" in posture_status else 'red'
            }
            detections.append(detection)
    
    return processed_frame, detections, posture_status

@app.route('/detect', methods=['POST'])
def detect_objects():
    """
    Main detection endpoint that processes images from Expo app
    """
    try:
        data = request.get_json()
        
        if 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode base64 image from Expo
        image_data = data['image']
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Get angles from request or use defaults
        lumbar_angle = data.get('lumbar_angle', 35)
        hip_angle = data.get('hip_angle', 18)
        
        # Process frame using your AR logic
        processed_frame, detections, posture_status = process_frame_with_ar(
            frame, lumbar_angle, hip_angle
        )
        
        # Encode processed frame as base64 for display in Expo
        _, buffer = cv2.imencode('.jpg', processed_frame)
        processed_image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            'success': True,
            'detections': detections,
            'posture_status': posture_status,
            'processed_image': processed_image_base64,
            'angles': {
                'lumbar_angle': lumbar_angle,
                'hip_angle': hip_angle
            },
            'count': len(detections)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'model_loaded': True,
        'keep_classes': keep_classes
    })

@app.route('/classes', methods=['GET'])
def get_classes():
    """Get available detection classes"""
    return jsonify({
        'all_classes': list(model.names.values()),
        'keep_classes': keep_classes
    })

# Your original scan_objects function for desktop use
def scan_objects():
    """
    Your original desktop scanning function
    Run this if you want to use webcam directly
    """
    cap = cv2.VideoCapture(1)  # Your original camera setup
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Use your original processing logic
        processed_frame, _, _ = process_frame_with_ar(frame)
        
        # Your original display code
        cv2.imshow("Maternal Wellness Demo", processed_frame)
        
        if cv2.waitKey(1) & 0xFF in [27, ord('q')]:  # ESC or q to quit
            break
    
    cap.release()
    cv2.destroyAllWindows()

def run_flask_server():
    """Run Flask server for Expo app"""
    print("Starting Flask server for Expo app...")
    print("Server running on http://0.0.0.0:5000")
    print("Available endpoints:")
    print("  POST /detect - Process images from Expo app")
    print("  GET /health - Health check")
    print("  GET /classes - Get detection classes")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        # Run Flask server for Expo app
        run_flask_server()
    else:
        # Run your original desktop version
        print("Running original desktop version...")
        print("Use 'python your_file.py server' to run Flask server for Expo app")
        scan_objects()

# Create model/posture_model.py if it doesn't exist
"""
# model/posture_model.py
def predict_posture(lumbar_angle, hip_angle):
    '''
    Your posture prediction logic
    Modify this based on your actual model
    '''
    # Example logic - replace with your actual implementation
    if lumbar_angle > 30 and hip_angle > 15:
        return "Safe Posture"
    elif lumbar_angle > 20 and hip_angle > 10:
        return "Moderate Risk"
    else:
        return "Poor Posture"
"""