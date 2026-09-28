import streamlit as st
import cv2
import time
from datetime import datetime
from ultralytics import YOLO

# Dashboard ki setting (Wide layout set karna)
st.set_page_config(page_title="AeroGuard Dashboard", layout="wide")

# Main Title
st.title("🚁 AeroGuard - AI Rescue Drone Dashboard")
st.markdown("**Smart India Hackathon 2026 | PS 177 - Ground Station UI**")
st.markdown("---")

# ==========================================
# MODEL LOAD FUNCTION
# ==========================================
# @st.cache_resource isliye lagaya hai taaki model baar-baar load na ho
@st.cache_resource
def load_yolo_model():
    return YOLO('yolov8n.pt')

model = load_yolo_model()

# ==========================================
# UI LAYOUT (2 Columns)
# ==========================================
# Left column video ke liye (70% space), Right column logs ke liye (30% space)
col1, col2 = st.columns([7, 3])

with col1:
    st.subheader("📡 Live Camera Feed")
    # Video frame ko baar-baar update karne ke liye ek khali jagah (placeholder) banate hain
    video_placeholder = st.empty()

with col2:
    st.subheader("🚨 Detection Logs")
    # Logs ko update karne ke liye placeholder
    log_placeholder = st.empty()

# ==========================================
# VIDEO STREAM & DETECTION LOGIC
# ==========================================
# ESP32-CAM IP URL yaha dalein (Testing ke liye 0 use karein laptop webcam ke liye)
STREAM_URL = 0 # "http://192.168.4.1:81/stream" 

# Start aur Stop button
start_button = st.sidebar.button("Start Rescue Mission ▶️")
stop_button = st.sidebar.button("Stop Mission ⏹️")

if start_button:
    cap = cv2.VideoCapture(STREAM_URL)
    
    # Logs ko store karne ke liye ek list
    detection_logs = []
    last_log_time = 0
    
    st.sidebar.success("Connection Established! Receiving Live Feed...")
    
    while cap.isOpened() and not stop_button:
        ret, frame = cap.read()
        if not ret:
            st.error("Drone camera feed lost. Please check connection.")
            break
            
        # YOLO Detection (Class 0 = Person)
        results = model.predict(source=frame, conf=0.5, classes=[0], verbose=False)
        annotated_frame = results[0].plot()
        
        # Log update logic (Agar koi insan detect hua)
        if len(results[0].boxes) > 0:
            current_time = time.time()
            # Har 3 second me ek hi log generate karega taaki screen spam na ho
            if current_time - last_log_time > 3:
                # Current time nikalna (e.g., 10:45:12 AM)
                timestamp = datetime.now().strftime("%I:%M:%S %p")
                new_log = f"⚠️ **{timestamp}** - Victim Detected!"
                
                # Naye log ko list me sabse upar add karna
                detection_logs.insert(0, new_log)
                last_log_time = current_time

        # OpenCV BGR format use karta hai, par Streamlit RGB samajhta hai, isliye color convert karna
        rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        
        # Left side me video update karna
        video_placeholder.image(rgb_frame, channels="RGB", use_container_width=True)
        
        # Right side me logs update karna
        log_text = ""
        # Sirf latest 10 logs dikhana taaki list zyada lambi na ho
        for log in detection_logs[:10]:
            log_text += f"{log} \n\n --- \n"
            
        if not log_text:
            log_placeholder.info("Scanning for victims... No detections yet.")
        else:
            log_placeholder.markdown(log_text)

    cap.release()
