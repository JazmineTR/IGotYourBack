import serial, time, re
from threading import Thread

latest_angles = (0.0, 0.0) 
latest_actuals = (0.0, 0.0, 0.0, 0.0, 0.0)

pattern = re.compile(r"(\w+):\s*(-?\d+(?:\.\d+)?)")
def parse(data: str):
    matches = pattern.findall(data)
    return {d: float(v) for d, v in matches}

def serial_loop(port='/dev/tty.usbmodem21101', baud_rate=115200):
    """ Continuously read serial and update latest_angles """
    global latest_angles
    global latest_actuals
    try:
        with serial.Serial(port, baud_rate, timeout=1) as arduino:
            time.sleep(2) 
            while True:
                inline = arduino.readline().decode('utf-8', errors="ignore").strip()
                if not inline:
                    continue
                dire = parse(inline)
                if dire:
                    R = dire.get("R", 0.0)
                    MB = dire.get("MB", 0.0)
                    MM = dire.get("MM", 0.0)
                    MT = dire.get("MT", 0.0)
                    L = dire.get("L", 0.0)

                    horizontal_avg = (R + MM + L) / 3
                    lumbar_angle = (horizontal_avg + MT) / 2
                    hip_angle = (MB + MM) / 2
                    latest_angles = (lumbar_angle, hip_angle)
                    latest_actuals = (R, MB, MM, MT, L)
    except Exception as e:
        print(f"[Serial error] {e}")

def start_serial_thread(port='/dev/tty.usbmodem21101', baud_rate=115200):
    thread = Thread(target=serial_loop, args=(port, baud_rate), daemon=True)
    thread.start()
    return thread

def get_latest_angles():
    return latest_angles

def get_latest_actuals():
    return latest_actuals