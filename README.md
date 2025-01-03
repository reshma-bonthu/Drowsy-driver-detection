# Driver Drowsiness Detection System

## Overview
The **Driver Drowsiness Detection System** is a computer vision-based application designed to enhance road safety by monitoring drivers for signs of drowsiness. Using real-time facial landmark detection, the system calculates the Eye Aspect Ratio (EAR) and Mouth Opening Ratio (MOR) to identify symptoms of fatigue, such as prolonged eye closure or yawning. When drowsiness is detected, the system issues alerts to prevent accidents.

---

## Features
- **Real-Time Monitoring**: Continuously tracks driver facial expressions using a webcam.
- **Drowsiness Detection**: Identifies signs of fatigue using EAR and MOR thresholds.
- **Alert System**: Triggers audio or visual alerts when drowsiness is detected.
- **User-Friendly Interface**: Displays live video feed with overlaid landmarks for easy visualization.
- **Extensible Framework**: Can be integrated with IoT devices or fleet management systems.

---

## Technologies Used
- **Programming Language**: Python
- **Libraries**:
  - OpenCV: For real-time video processing and facial landmark detection.
  - dlib: For detecting facial landmarks.
  - NumPy: For numerical computations.
- **Hardware**: Standard webcam or any compatible video capturing device.
---

## How It Works
1. **Facial Landmark Detection**: Uses dlib's pre-trained models to detect facial landmarks.
2. **Eye Aspect Ratio (EAR)**: Calculates the ratio of eye width to height to determine if the eyes are closed.
3. **Mouth Opening Ratio (MOR)**: Analyzes the distance between upper and lower lip to detect yawning.
4. **Threshold-Based Alerts**: Triggers alerts if EAR or MOR exceeds predefined thresholds.

