import cv2
from ultralytics import YOLO

def draw_custom_boxes(frame, model):
    """
    Live video frame me detect hue objects ke aaju-baju custom Bounding Boxes (rectangles) draw karna.
    """
    
    # Model ko frame pass karna
    results = model.predict(source=frame, conf=0.5, verbose=False)
    
    # Results se bounding boxes ka data nikalna
    boxes = results[0].boxes
    
    # Har detected object ke upar loop lagana
    for box in boxes:
        # Bounding box ke 4 coordinates nikalna (x1, y1 = top-left; x2, y2 = bottom-right)
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        
        # Object ka confidence score (jaise 0.85 = 85%) nikalna
        conf = float(box.conf[0])
        
        # Object ki Class ID nikalna (0 = Person)
        cls_id = int(box.cls[0])
        
        # Default colors (Blue box)
        box_color = (255, 0, 0) # BGR format: Blue
        label = f"Unknown: {conf:.2f}"
        
        # 1. PERSON detected (Green Box)
        if cls_id == 0:
            box_color = (0, 255, 0) # BGR: Green
            label = f"VICTIM: {conf:.2f}"
            
        # 2. FIRE detected (Red Box) - Note: Default model me fire nahi hoti
        elif cls_id == 1: 
            box_color = (0, 0, 255) # BGR: Red
            label = f"FIRE DANGER: {conf:.2f}"

        # ---------------------------------------------------------
        # BOUNDING BOX (Rectangle) DRAW KARNA
        # cv2.rectangle(image, start_point, end_point, color, thickness)
        # ---------------------------------------------------------
        cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
        
        # ---------------------------------------------------------
        # BOX KE UPAR LABEL (Text Box) DRAW KARNA
        # ---------------------------------------------------------
        # Text ka size check karna taaki background thik se bane
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
        
        # Label ke background ke liye ek solid rectangle draw karna
        cv2.rectangle(frame, (x1, y1 - 20), (x1 + text_size[0], y1), box_color, -1)
        
        # Text ko box ke andar white color se likhna
        cv2.putText(frame, label, (x1, y1 - 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    
    return frame

# ==========================================
# TEST KARNE KE LIYE CODE
# ==========================================
if __name__ == "__main__":
    print("Loading YOLOv8 Model...")
    rescue_model = YOLO('yolov8n.pt') 
    
    # 0 for webcam, ya phir yaha ESP32-CAM ka IP URL dalein (e.g. "http://192.168.4.1:81/stream")
    cap = cv2.VideoCapture(0) 
    
    while True:
        ret, current_frame = cap.read()
        if not ret: break
        
        # Custom Bounding Box function ko call karna
        final_frame = draw_custom_boxes(current_frame, rescue_model)
        
        cv2.imshow("AeroGuard Bounding Box Test", final_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
