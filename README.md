# Driver_Drowsiness_Detection
# Driver Drowsiness Detection System Using CNN and OpenCV

This project implements a real-time driver drowsiness detection system using computer vision and deep learning.

---

## Overview

- Detects open or closed eyes from webcam video feed using Haar cascades and a trained CNN model.
- Raises an alarm sound when driver’s eyes are closed for a continuous period, indicating drowsiness.
- Sends a sleep alert message via MQTT to a remote broker for monitoring.
- Saves a snapshot of the frame when drowsiness is detected.
- Provides visual feedback with bounding boxes and status on the video window.

---

## Folder Structure

- `alarms/`: Alarm sound files
- `cascades/`: Haar cascade XML files for face and eye detection
- `models/`: Pre-trained CNN model file
- `results/`: Saved images during alerts
- `src/`: Source code files (modular)
- `requirements.txt`: Python dependencies
- `run.py`: Script to start detection

---

## Installation

1. Clone the repo:

```bash
git clone https://github.com/Rania334/Driver_Drowsiness_Detection.git
cd Driver_Drowsiness_Detection
