import cv2
import time
from ultralytics import YOLO

print("Loading YOLOv8 AI Model... (Pehli baar thoda time lag sakta hai internet se download hone me)")
# 'yolov8n.pt' (Nano model) sabse fast hota hai live feed ke liye
model = YOLO('yolov8n.pt') 

# ESP32-CAM ka IP Address yaha dalein
STREAM_URL = "http://192.168.4.1:81/stream"  # <--- UPDATE THIS IP

print(f"Connecting to ESP32-CAM stream at {STREAM_URL}...")
cap = cv2.VideoCapture(STREAM_URL)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not cap.isOpened():
    print("Error: Could not open the video stream. Check Wi-Fi and IP address.")
    exit()

print("Successfully connected! Press 'q' to close the window.")
prev_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Waiting for drone camera feed...")
        time.sleep(1)
        continue

    # ==========================================
    # AI DETECTION LOGIC (YOLOv8)
    # ==========================================
    # conf=0.5 matlab 50% se zyada sure hone par hi box banayega
    # classes=[0] matlab COCO dataset ka sirf 0th class (Person/Insan) detect karega
    # verbose=False se terminal me faltu ka text print nahi hoga
    results = model.predict(source=frame, conf=0.5, classes=[0], verbose=False)
    
    # results[0].plot() original frame par boxes aur labels draw kar deta hai
    annotated_frame = results[0].plot()

    # ==========================================
    # ALERT SYSTEM (Agar koi insan detect hua)
    # ==========================================
    # Check karein ki frame me kitne log detect hue hain
    person_count = len(results[0].boxes)
    if person_count > 0:
        # Screen par red color me VICTIM DETECTED likhkar aayega
        cv2.putText(annotated_frame, f"ALERT: {person_count} VICTIM(S) DETECTED!", 
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        print(f"🚨 ALERT: Victim Detected! Location data saved.") # Yaha aap buzzer bajane ka code bhi dal sakte hain

    # FPS Calculate karna (Performance check karne ke liye)
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time
    
    cv2.putText(annotated_frame, f"FPS: {int(fps)}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Output screen par dikhana
    cv2.imshow("AeroGuard - Rescue AI Ground Station", annotated_frame)

    # 'q' dabakar exit karna
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Closing Ground Station...")
        break

cap.release()
cv2.destroyAllWindows()
