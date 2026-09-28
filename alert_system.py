import cv2
import time
import threading
from ultralytics import YOLO

# Windows OS ke liye inbuilt sound library (Agar Mac/Linux hai toh 'playsound' library use karni padegi)
try:
    import winsound
except ImportError:
    winsound = None

# Background me beep bajane ka function (taaki video hang na ho)
def play_beep():
    if winsound:
        # Frequency = 2000 Hz, Duration = 300 milliseconds
        winsound.Beep(2000, 300) 
    else:
        print("Beep! (Audio alert not supported on this OS without extra libraries)")

def run_alert_system():
    print("Loading YOLOv8 Rescue Model...")
    model = YOLO('yolov8n.pt') 
    
    # Testing ke liye laptop webcam (0). Drone ke liye yahan URL dalein: "http://192.168.x.x:81/stream"
    cap = cv2.VideoCapture(0)
    
    # Flashing effect ke liye variables
    flash_state = False
    last_toggle_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # AI Detection sirf Person (class 0) ke liye
        results = model.predict(source=frame, conf=0.5, classes=[0], verbose=False)
        annotated_frame = results[0].plot()
        
        # Check karna ki frame me koi person detect hua hai ya nahi
        person_detected = len(results[0].boxes) > 0
        current_time = time.time()
        
        if person_detected:
            # Har 0.4 seconds me flash state ko ON/OFF toggle karna
            if current_time - last_toggle_time > 0.4:
                flash_state = not flash_state
                last_toggle_time = current_time
                
                # Jab flash ON ho, tabhi beep bajana (har 0.8 second me ek beep)
                if flash_state:
                    threading.Thread(target=play_beep, daemon=True).start()
            
            # Agar flash_state True hai, toh screen par bada lal text dikhana
            if flash_state:
                # Text ko shadow effect dene ke liye pehle black text, phir red text draw karte hain
                cv2.putText(annotated_frame, "!!! VICTIM DETECTED !!!", (50, 100), 
                            cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 0), 5) # Black shadow
                cv2.putText(annotated_frame, "!!! VICTIM DETECTED !!!", (50, 100), 
                            cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 255), 3) # Red main text
                
                # Screen ke border par red color ka danger frame draw karna
                cv2.rectangle(annotated_frame, (0, 0), (annotated_frame.shape[1], annotated_frame.shape[0]), 
                              (0, 0, 255), 10)
        else:
            # Agar koi detect nahi hua, toh flash state reset kar dena
            flash_state = False
            
        cv2.imshow("AeroGuard Alert System", annotated_frame)
        
        # 'q' dabakar quit karne ka logic
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_alert_system()
