# AeroGuard - Cost-Effective AI Rescue Drone 🚁

**Smart India Hackathon (SIH) 2026**  
**Problem Statement:** PS 177 (Qualcomm Inc) - Deployable AI-powered autonomous drone for search-and-rescue operations.  
**Theme:** Robotics and Drones  
**Team Name:** Team MechScribe

## 📌 Project Overview
AeroGuard is a cost-effective, semi-autonomous drone designed to assist in disaster zones (earthquakes, landslides, floods). Instead of using expensive onboard processing, we utilize an **ESP32-CAM** to stream live video to a ground station (laptop). The ground station runs **YOLOv8** and **OpenCV** to detect humans and hazards in real-time.

## 🛠️ Technical Stack
* **Hardware:** F450 Drone Frame, BLDC Motors, F405 Flight Controller, ESP32-CAM Module.
* **Software (AI):** Python, OpenCV, YOLOv8 (Ultralytics).
* **Communication:** Local Wi-Fi Video Streaming.
* **Design:** SolidWorks (CAD for 3D printed mounts and payload drop).

## 👥 Team Roles
* **Mechanical Design & CAD:** Shubham Gaikwad, Vidhi Naresh Kaikadi
* **Hardware Assembly:** Vijay Mahendra Kanojiya
* **AI & Software:** Nikita Shainath Salunke, Roshan Avinash Kinge
* **Documentation & Pitch:** Yash Rahul Holkar

## 📂 Folder Structure
* `/hardware` - CAD files (SolidWorks/Fusion360) and circuit diagrams.
* `/esp32_cam` - Arduino code for video streaming.
* `/ground_station_ai` - Python scripts for OpenCV and YOLO detection.
