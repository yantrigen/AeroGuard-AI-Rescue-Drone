# 1. Ultralytics library se YOLO class ko import karein
from ultralytics import YOLO

print("YOLOv8 Model Load ho raha hai...")

# 2. YOLOv8 ka Nano model (yolov8n.pt) load karein
model = YOLO('yolov8n.pt')

print("Model successfully load ho gaya!")
