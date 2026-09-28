import cv2
from ultralytics import YOLO

def detect_objects_and_hazards(frame, model):
    """
    Live video frame ko YOLO model me bhejkar Person aur Fire/Smoke detect karne ka logic.
    """
    
    # YOLO model ko frame pass karna
    # conf=0.45: Agar AI 45% se zyada sure hai tabhi detection dikhayega
    # classes=[0, 15, 16]: COCO dataset me 0=Person. (Note: Standard COCO me fire nahi hoti, 
    # agar aapne custom model (e.g., 'fire_detect.pt') train kiya hai toh class IDs change hongi)
    results = model.predict(source=frame, conf=0.45, verbose=False)
    
    # Frame par detected objects ke boxes aur labels draw karna
    annotated_frame = results[0].plot()
    
    # Detection results analyze karna
    detected_classes = results[0].boxes.cls.tolist() # Frame me kya mila uski list
    
    person_detected = False
    hazard_detected = False
    
    for cls_id in detected_classes:
        # Class 0 generally 'Person' ke liye hota hai
        if int(cls_id) == 0:
            person_detected = True
            
        # Agar aapka model custom hai, toh aap Fire/Smoke ki class ID yaha set karenge (e.g., Class 1)
        elif int(cls_id) == 1: 
            hazard_detected = True

    # Alert System
    if person_detected:
        cv2.putText(annotated_frame, "ALERT: VICTIM DETECTED!", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    
    if hazard_detected:
        cv2.putText(annotated_frame, "DANGER: FIRE/SMOKE DETECTED!", (20, 90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 3) # Orange warning

    return annotated_frame, person_detected, hazard_detected

# Example Usage (Main loop ke andar ise call karenge)
if __name__ == "__main__":
    print("Loading AI Model...")
    # NOTE: Fire/Smoke detection ke liye ek custom trained model '.pt' file leni padegi, 
    # filhal testing ke liye default yolov8n use kar rahe hain
    rescue_model = YOLO('yolov8n.pt') 
    
    cap = cv2.VideoCapture(0) # 0 for laptop webcam test
    
    while True:
        ret, current_frame = cap.read()
        if not ret: break
        
        # Detection logic function ko call karna
        processed_frame, found_person, found_fire = detect_objects_and_hazards(current_frame, rescue_model)
        
        cv2.imshow("AeroGuard Detection Feed", processed_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
