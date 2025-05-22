import numpy as np
import cv2

def preprocess_eye(eye_img):
    eye_gray = cv2.cvtColor(eye_img, cv2.COLOR_BGR2GRAY)
    eye_resized = cv2.resize(eye_gray, (100, 100))
    eye_normalized = eye_resized / 255.0
    eye_reshaped = eye_normalized.reshape(100, 100, -1)
    return np.expand_dims(eye_reshaped, axis=0)

def draw_rectangles(frame, detections, color=(150, 150, 150)):
    for (x, y, w, h) in detections:
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 1)
