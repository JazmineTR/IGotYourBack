from model.posture_model import *
from force_reader import get_latest_angles, start_serial_thread
import cv2
import time

start_serial_thread()
danger_start_time = None
danger_threshold_sec = 10

while True:
    lumbar_angle, hip_angle = get_latest_angles()
    posture_status = predict_posture(lumbar_angle, hip_angle)

    if "Dangerous" in posture_status:
        if danger_start_time is None:
            danger_start_time = time.time()
        elif time.time() - danger_start_time >= danger_threshold_sec:
            posture_status = "Dangerous (10s+)"
    else:
        danger_start_time = None

    print(f"Lumbar={lumbar_angle:.2f}, Hip={hip_angle:.2f} → {posture_status}")

    if cv2.waitKey(1) & 0xFF in [27, ord('q')]:  # ESC or q
        break 

    time.sleep(0.1)
